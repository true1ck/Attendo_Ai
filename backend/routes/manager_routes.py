"""
Manager Routes
Handles manager dashboard, AI insights, mismatches, and approval functionality
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date
from backend.models import (
    Manager, Vendor, DailyStatus, MismatchRecord, SwipeRecord, AuditLog,
    UserRole, AttendanceStatus, ApprovalStatus
)
from backend.extensions import db
from backend.utils.helpers import create_audit_log

# Create manager blueprint
manager_bp = Blueprint('manager', __name__, url_prefix='/manager')


@manager_bp.route('/dashboard')
@login_required
def dashboard():
    """Manager dashboard with real team data"""
    if current_user.role != UserRole.MANAGER:
        flash('Access denied', 'error')
        return redirect(url_for('auth.index'))
    
    manager = current_user.manager_profile
    if not manager:
        flash('Manager profile not found', 'error')
        return redirect(url_for('auth.login'))
    
    # Get team statistics
    today = date.today()
    team_vendors = manager.team_vendors.all() if manager.team_vendors else []
    vendor_ids = [v.id for v in team_vendors]
    
    # Get today's statuses for team
    today_statuses = []
    present_count = 0
    pending_approvals = 0
    mismatches_count = 0
    
    for vendor in team_vendors:
        # Get today's status
        today_status = DailyStatus.query.filter_by(
            vendor_id=vendor.id, 
            status_date=today
        ).first()
        
        if today_status:
            if today_status.status in [AttendanceStatus.IN_OFFICE_FULL, AttendanceStatus.IN_OFFICE_HALF, 
                                     AttendanceStatus.WFH_FULL, AttendanceStatus.WFH_HALF]:
                present_count += 1
            if today_status.approval_status == ApprovalStatus.PENDING:
                pending_approvals += 1
                
        # Get pending mismatches for this vendor
        vendor_mismatches = MismatchRecord.query.filter_by(
            vendor_id=vendor.id,
            manager_approval=ApprovalStatus.PENDING
        ).count()
        mismatches_count += vendor_mismatches
        
        # Add to today's status list
        today_statuses.append({
            'vendor': vendor,
            'status': today_status,
            'has_mismatch': vendor_mismatches > 0
        })
    
    # Pending approvals for the team (recent)
    pending_statuses = []
    if vendor_ids:
        pending_statuses = DailyStatus.query.filter(
            DailyStatus.vendor_id.in_(vendor_ids),
            DailyStatus.approval_status == ApprovalStatus.PENDING
        ).order_by(DailyStatus.status_date.desc(), DailyStatus.submitted_at.desc()).limit(50).all()
    
    team_stats = {
        'total_members': len(team_vendors),
        'present_today': present_count,
        'pending_approvals': pending_approvals,
        'mismatches': mismatches_count
    }
    
    return render_template('manager_dashboard.html', 
                         manager=manager,
                         team_stats=team_stats,
                         today_statuses=today_statuses,
                         pending_statuses=pending_statuses,
                         today_date=today.strftime('%B %d, %Y'))


@manager_bp.route('/ai-insights')
@login_required
def ai_insights():
    """AI Insights page backed by heuristic predictions."""
    if current_user.role != UserRole.MANAGER:
        flash('Access denied', 'error')
        return redirect(url_for('auth.index'))

    manager = current_user.manager_profile
    if not manager:
        flash('Manager profile not found', 'error')
        return redirect(url_for('auth.login'))

    try:
        # Import from utils (need to access the original utils.py)
        import sys, os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from utils import generate_ai_insights
        
        # Optional query param to adjust window (days)
        window = request.args.get('window', default='7')
        try:
            prediction_window = max(3, min(30, int(window)))
        except Exception:
            prediction_window = 7

        predictions, ai_stats, risk_distribution = generate_ai_insights(manager.id, prediction_window_days=prediction_window)

        return render_template(
            'ai_insights.html',
            ai_stats=ai_stats,
            predictions=predictions,
            risk_distribution=risk_distribution
        )
    except Exception as e:
        flash(f'Error loading AI insights: {str(e)}', 'error')
        # Fallback to template with no data (will show demo placeholders)
        return render_template('ai_insights.html', ai_stats={}, predictions=[], risk_distribution={})


@manager_bp.route('/mismatches')
@login_required
def mismatches():
    """Review attendance mismatches between swipe records and submitted status"""
    if current_user.role != UserRole.MANAGER:
        flash('Access denied', 'error')
        return redirect(url_for('auth.index'))
    
    manager = current_user.manager_profile
    if not manager:
        flash('Manager profile not found', 'error')
        return redirect(url_for('auth.login'))
    
    # Get filters
    status_filter = request.args.get('status', 'pending')
    vendor_filter = request.args.get('vendor', 'all')
    
    # Get team vendors
    team_vendors = manager.team_vendors.all()
    vendor_ids = [v.id for v in team_vendors]
    
    # Build query for mismatches
    mismatch_query = MismatchRecord.query.filter(
        MismatchRecord.vendor_id.in_(vendor_ids)
    )
    
    if status_filter != 'all':
        if status_filter == 'pending':
            mismatch_query = mismatch_query.filter(
                MismatchRecord.manager_approval == ApprovalStatus.PENDING
            )
        elif status_filter == 'approved':
            mismatch_query = mismatch_query.filter(
                MismatchRecord.manager_approval == ApprovalStatus.APPROVED
            )
        elif status_filter == 'rejected':
            mismatch_query = mismatch_query.filter(
                MismatchRecord.manager_approval == ApprovalStatus.REJECTED
            )
    
    if vendor_filter != 'all':
        vendor = next((v for v in team_vendors if v.vendor_id == vendor_filter), None)
        if vendor:
            mismatch_query = mismatch_query.filter(MismatchRecord.vendor_id == vendor.id)
    
    # Get mismatches with vendor details
    mismatches = mismatch_query.order_by(MismatchRecord.mismatch_date.desc()).all()
    
    # Group mismatches by vendor
    vendor_mismatches = {}
    for mismatch in mismatches:
        vendor_id = mismatch.vendor.vendor_id
        if vendor_id not in vendor_mismatches:
            vendor_mismatches[vendor_id] = {
                'vendor': mismatch.vendor,
                'mismatches': [],
                'pending_count': 0,
                'total_count': 0
            }
        
        vendor_mismatches[vendor_id]['mismatches'].append(mismatch)
        vendor_mismatches[vendor_id]['total_count'] += 1
        if mismatch.manager_approval == ApprovalStatus.PENDING:
            vendor_mismatches[vendor_id]['pending_count'] += 1
    
    # Calculate summary stats
    total_mismatches = len(mismatches)
    pending_mismatches = len([m for m in mismatches if m.manager_approval == ApprovalStatus.PENDING])
    vendors_with_mismatches = len(vendor_mismatches)
    
    summary_stats = {
        'total_mismatches': total_mismatches,
        'pending_mismatches': pending_mismatches,
        'vendors_affected': vendors_with_mismatches,
        'resolution_rate': round((total_mismatches - pending_mismatches) / total_mismatches * 100, 1) if total_mismatches > 0 else 100
    }
    
    return render_template('manager_mismatches.html',
                         manager=manager,
                         vendor_mismatches=vendor_mismatches,
                         summary_stats=summary_stats,
                         status_filter=status_filter,
                         vendor_filter=vendor_filter,
                         team_vendors=team_vendors,
                         approval_statuses=ApprovalStatus)


@manager_bp.route('/mismatches/table')
@login_required
def mismatches_table():
    """Manager's team mismatches in table format (similar to admin reconciliation)"""
    if current_user.role != UserRole.MANAGER:
        flash('Access denied', 'error')
        return redirect(url_for('auth.index'))
    
    manager = current_user.manager_profile
    if not manager:
        flash('Manager profile not found', 'error')
        return redirect(url_for('auth.login'))
    
    # Get filters
    status_filter = request.args.get('status', 'all')
    vendor_filter = request.args.get('vendor', 'all')
    conflict_filter = request.args.get('conflict', 'all')
    
    # Get team vendors
    team_vendors = manager.team_vendors.all()
    vendor_ids = [v.id for v in team_vendors]
    
    # Build query for mismatches
    mismatch_query = MismatchRecord.query.filter(
        MismatchRecord.vendor_id.in_(vendor_ids)
    )
    
    # Apply status filter
    if status_filter != 'all':
        if status_filter == 'pending':
            mismatch_query = mismatch_query.filter(
                MismatchRecord.manager_approval == ApprovalStatus.PENDING
            )
        elif status_filter == 'approved':
            mismatch_query = mismatch_query.filter(
                MismatchRecord.manager_approval == ApprovalStatus.APPROVED
            )
        elif status_filter == 'rejected':
            mismatch_query = mismatch_query.filter(
                MismatchRecord.manager_approval == ApprovalStatus.REJECTED
            )
    
    # Apply vendor filter
    if vendor_filter != 'all':
        vendor = next((v for v in team_vendors if v.vendor_id == vendor_filter), None)
        if vendor:
            mismatch_query = mismatch_query.filter(MismatchRecord.vendor_id == vendor.id)
    
    # Get mismatches ordered by date (latest first)
    mismatches = mismatch_query.order_by(MismatchRecord.mismatch_date.desc()).limit(100).all()
    
    # Apply conflict filter after fetching (since it's based on logic)
    if conflict_filter != 'all':
        filtered_mismatches = []
        for m in mismatches:
            priority = 'low'  # default
            if m.web_status and m.swipe_status:
                if (m.web_status.value in ['wfh_full', 'wfh_half', 'leave_full', 'leave_half'] and m.swipe_status == 'AP'):
                    priority = 'high'
                elif (m.web_status.value in ['in_office_full', 'in_office_half'] and m.swipe_status == 'AA'):
                    priority = 'medium'
            
            if conflict_filter == priority:
                filtered_mismatches.append(m)
        
        mismatches = filtered_mismatches
    
    # Calculate summary stats
    total_mismatches = len(mismatches)
    pending_mismatches = len([m for m in mismatches if m.manager_approval == ApprovalStatus.PENDING])
    approved_mismatches = len([m for m in mismatches if m.manager_approval == ApprovalStatus.APPROVED])
    team_members_count = len(team_vendors)
    
    summary = {
        'total': total_mismatches,
        'pending': pending_mismatches,
        'approved': approved_mismatches,
        'team_members': team_members_count
    }
    
    return render_template('manager_mismatches_table.html',
                         mismatches=mismatches,
                         summary=summary,
                         status_filter=status_filter,
                         vendor_filter=vendor_filter,
                         conflict_filter=conflict_filter,
                         team_vendors=team_vendors)


@manager_bp.route('/mismatch/<int:mismatch_id>/approve', methods=['POST'])
@login_required
def approve_mismatch_explanation(mismatch_id):
    """Approve vendor's mismatch explanation"""
    if current_user.role != UserRole.MANAGER:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        mismatch = MismatchRecord.query.get_or_404(mismatch_id)
        manager = current_user.manager_profile
        
        # Verify vendor is in manager's team
        if mismatch.vendor.manager_id != manager.manager_id:
            return jsonify({'error': 'You can only review mismatches for your team members'}), 403
        
        action = request.form.get('action')
        manager_comments = request.form.get('comments', '')
        
        if action == 'approve':
            mismatch.manager_approval = ApprovalStatus.APPROVED
            message = 'Mismatch explanation approved'
        elif action == 'reject':
            mismatch.manager_approval = ApprovalStatus.REJECTED
            message = 'Mismatch explanation rejected'
        else:
            return jsonify({'error': 'Invalid action'}), 400
        
        mismatch.manager_comments = manager_comments
        mismatch.approved_by = current_user.id
        mismatch.approved_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit log
        create_audit_log(current_user.id, action.upper(), 'mismatch_records', mismatch_id,
                       {'manager_approval': 'pending'}, 
                       {'manager_approval': action, 'manager_comments': manager_comments})
        
        return jsonify({
            'status': 'success',
            'message': message,
            'action': action,
            'mismatch_id': mismatch_id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@manager_bp.route('/billing-corrections', methods=['GET', 'POST'])
@login_required
def billing_corrections():
    """Manager billing corrections for their team members only"""
    if current_user.role != UserRole.MANAGER:
        flash('Access denied', 'error')
        return redirect(url_for('auth.index'))
    
    manager = current_user.manager_profile
    if not manager:
        flash('Manager profile not found', 'error')
        return redirect(url_for('auth.login'))
    
    # Get team vendors for validation and dropdown
    team_vendors = manager.team_vendors.all()
    team_vendor_ids = {v.vendor_id: v.id for v in team_vendors}
    
    if request.method == 'POST':
        try:
            vendor_id = request.form['vendor_id']
            date_str = request.form['date']
            corrected_hours = float(request.form['corrected_hours'])
            reason = request.form.get('reason', '')
            
            # Validate vendor belongs to manager's team
            if vendor_id not in team_vendor_ids:
                flash('You can only correct billing for your team members', 'error')
                return redirect(url_for('manager.billing_corrections'))
            
            vendor = Vendor.query.filter_by(vendor_id=vendor_id).first()
            if not vendor:
                flash('Vendor not found', 'error')
                return redirect(url_for('manager.billing_corrections'))
            
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
                'correction_type': 'manager_correction',
                'corrected_by': current_user.username
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
    
    # Show corrections for manager's team only
    corrections = AuditLog.query.filter(
        AuditLog.action == 'BILLING_CORRECTION',
        AuditLog.record_id.in_(team_vendor_ids.values())
    ).order_by(AuditLog.created_at.desc()).limit(50).all()
    
    return render_template('manager_billing_corrections.html', 
                         corrections=corrections,
                         team_vendors=team_vendors,
                         manager=manager)
