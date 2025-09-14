"""
Admin Routes
Handles admin dashboard, system management, and administrative functionality
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date, timedelta
from backend.models import (
    User, Vendor, Manager, DailyStatus, SwipeRecord, Holiday,
    MismatchRecord, AuditLog, UserRole, ApprovalStatus
)
from backend.extensions import db
from backend.utils.helpers import create_audit_log

# Create admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Global variables for Excel sync status (maintained from original)
excel_sync_status = {
    'last_sync': None,
    'status': 'Stopped',
    'files_synced': 0,
    'errors': []
}
excel_sync_running = False


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    if current_user.role != UserRole.ADMIN:
        flash('Access denied', 'error')
        return redirect(url_for('auth.index'))
    
    # Get statistics
    total_vendors = Vendor.query.count()
    total_managers = Manager.query.count()
    total_statuses_today = DailyStatus.query.filter_by(status_date=date.today()).count()
    
    # Upcoming holidays (next 5)
    upcoming_holidays = Holiday.query.filter(
        Holiday.holiday_date >= date.today()
    ).order_by(Holiday.holiday_date.asc()).limit(5).all()
    
    # Get persistent system issues from database
    try:
        from system_issues import SystemIssueManager, report_excel_sync_error, report_database_error, report_service_down
        
        # Check for new issues and report them
        
        # 1. Check Excel sync errors
        if excel_sync_status.get('errors') and len(excel_sync_status['errors']) > 0:
            latest_error = excel_sync_status['errors'][-1]
            report_excel_sync_error(latest_error)
        
        # 2. Check if Excel sync service should be running but isn't
        from flask import current_app
        if current_app.config.get('EXCEL_NETWORK_FOLDER') and not excel_sync_running:
            report_service_down("Excel Sync Service")
        
        # 3. Test database connectivity
        try:
            test_count = db.session.query(User).count()
            if test_count < 0:  # Invalid result
                report_database_error("Database query returned invalid results")
        except Exception as e:
            report_database_error(str(e))
        
        # Get current active issues
        system_issues = SystemIssueManager.get_active_issues_count()
        active_issues = SystemIssueManager.get_active_issues()
        
    except ImportError:
        # Fallback if system_issues module not available
        system_issues = 0
        active_issues = []
    
    # Get business workflow metrics (separate from system issues)
    pending_mismatches = MismatchRecord.query.filter_by(manager_approval=ApprovalStatus.PENDING).count()
    
    # Create system stats object for template
    system_stats = {
        'total_vendors': total_vendors,
        'total_managers': total_managers,
        'todays_submissions': total_statuses_today,
        'system_issues': system_issues,
        'active_issues': [issue.to_dict() for issue in active_issues] if 'active_issues' in locals() else [],
        'pending_mismatches': pending_mismatches  # Business metric, not system issue
    }
    
    return render_template('admin_dashboard.html',
                         system_stats=system_stats,
                         total_vendors=total_vendors,
                         total_managers=total_managers,
                         total_statuses_today=total_statuses_today,
                         upcoming_holidays=upcoming_holidays)


@admin_bp.route('/holidays')
@login_required
def holidays():
    """Admin holidays management page"""
    if current_user.role != UserRole.ADMIN:
        flash('Access denied', 'error')
        return redirect(url_for('auth.index'))
    holidays = Holiday.query.order_by(Holiday.holiday_date.asc()).all()
    return render_template('admin_holidays.html', holidays=holidays)


@admin_bp.route('/system-settings')
@login_required
def system_settings():
    """Admin system settings page (bulk import, templates)"""
    if current_user.role != UserRole.ADMIN:
        flash('Access denied', 'error')
        return redirect(url_for('auth.index'))
    return render_template('admin_system_settings.html')


@admin_bp.route('/audit-logs')
@login_required
def audit_logs():
    """Admin audit logs page"""
    if current_user.role != UserRole.ADMIN:
        flash('Access denied', 'error')
        return redirect(url_for('auth.index'))
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(200).all()
    return render_template('admin_audit_logs.html', logs=logs)


@admin_bp.route('/teams')
@login_required
def teams():
    """Admin teams & groups management"""
    if current_user.role != UserRole.ADMIN:
        flash('Access denied', 'error')
        return redirect(url_for('auth.index'))
    managers = Manager.query.all()
    # Build summary by manager and department
    team_data = []
    for m in managers:
        members = m.team_vendors.all() if m.team_vendors else []
        dept_counts = {}
        for v in members:
            dept_counts[v.department] = dept_counts.get(v.department, 0) + 1
        team_data.append({'manager': m, 'members': members, 'dept_counts': dept_counts})
    return render_template('admin_teams.html', team_data=team_data)


@admin_bp.route('/reconciliation')
@login_required
def reconciliation():
    """Admin reconciliation report page"""
    if current_user.role != UserRole.ADMIN:
        flash('Access denied', 'error')
        return redirect(url_for('auth.index'))
    # Load latest mismatches (limit for performance)
    mismatches = MismatchRecord.query.order_by(MismatchRecord.mismatch_date.desc()).limit(500).all()
    total = len(mismatches)
    pending = len([m for m in mismatches if m.manager_approval == ApprovalStatus.PENDING])
    approved = len([m for m in mismatches if m.manager_approval == ApprovalStatus.APPROVED])
    rejected = len([m for m in mismatches if m.manager_approval == ApprovalStatus.REJECTED])
    summary = {
        'total': total,
        'pending': pending,
        'approved': approved,
        'rejected': rejected
    }
    return render_template('admin_reconciliation.html', mismatches=mismatches, summary=summary)


@admin_bp.route('/billing-corrections', methods=['GET', 'POST'])
@login_required
def billing_corrections():
    """Admin billing corrections (offsets)"""
    if current_user.role != UserRole.ADMIN:
        flash('Access denied', 'error')
        return redirect(url_for('auth.index'))
    if request.method == 'POST':
        try:
            vendor_id = request.form['vendor_id']
            date_str = request.form['date']
            corrected_hours = float(request.form['corrected_hours'])
            reason = request.form.get('reason', '')
            vendor = Vendor.query.filter_by(vendor_id=vendor_id).first()
            if not vendor:
                flash('Vendor not found', 'error')
                return redirect(url_for('admin.billing_corrections'))
            
            # Try to get existing hours for this vendor on this date
            correction_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            existing_status = DailyStatus.query.filter_by(
                vendor_id=vendor.id, 
                status_date=correction_date
            ).first()
            
            # Capture old values for comparison
            old_values = {}
            if existing_status and existing_status.total_hours:
                old_values['previous_hours'] = existing_status.total_hours
                old_values['vendor_id'] = vendor_id
                old_values['date'] = date_str
                old_values['status'] = existing_status.status.value if existing_status.status else None
            else:
                # Check swipe records for historical data
                swipe_record = SwipeRecord.query.filter_by(
                    vendor_id=vendor.id,
                    attendance_date=correction_date
                ).first()
                if swipe_record and swipe_record.total_hours:
                    old_values['previous_hours'] = swipe_record.total_hours
                    old_values['source'] = 'swipe_record'
                old_values['vendor_id'] = vendor_id
                old_values['date'] = date_str
            
            # Log correction in audit log with proper old/new values comparison
            new_values = {
                'vendor_id': vendor_id,
                'date': date_str,
                'corrected_hours': corrected_hours,
                'reason': reason,
                'correction_type': 'manual_override'
            }
            
            create_audit_log(current_user.id,
                             'BILLING_CORRECTION',
                             'billing',
                             vendor.id,
                             old_values,
                             new_values)
            
            # Create informative success message
            if old_values.get('previous_hours'):
                success_msg = f'Billing correction recorded: {vendor_id} on {date_str} updated from {old_values["previous_hours"]} hrs to {corrected_hours} hrs'
            else:
                success_msg = f'Billing correction recorded: {vendor_id} on {date_str} set to {corrected_hours} hrs (new entry)'
            
            flash(success_msg, 'success')
        except Exception as e:
            flash(f'Error recording correction: {str(e)}', 'error')
    # Show last 50 corrections from audit logs
    corrections = AuditLog.query.filter(AuditLog.action == 'BILLING_CORRECTION').order_by(AuditLog.created_at.desc()).limit(50).all()
    return render_template('admin_billing_corrections.html', corrections=corrections)
