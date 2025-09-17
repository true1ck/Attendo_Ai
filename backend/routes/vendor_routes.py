"""
Vendor Routes
Handles vendor dashboard and vendor-specific functionality
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date
from backend.models import (
    Vendor, Manager, DailyStatus, MismatchRecord, Holiday,
    UserRole, ApprovalStatus
)

# Create vendor blueprint
vendor_bp = Blueprint('vendor', __name__, url_prefix='/vendor')


@vendor_bp.route('/dashboard')
@login_required
def dashboard():
    """Vendor dashboard showing status submission and history"""
    if current_user.role != UserRole.VENDOR:
        flash('Access denied', 'error')
        return redirect(url_for('auth.index'))
    
    vendor = current_user.vendor_profile
    if not vendor:
        flash('Vendor profile not found', 'error')
        return redirect(url_for('auth.login'))
    
    # Get manager information
    manager = None
    if vendor.manager_id:
        manager = Manager.query.filter_by(manager_id=vendor.manager_id).first()
    
    # Get today's status
    today = date.today()
    today_status = DailyStatus.query.filter_by(
        vendor_id=vendor.id, 
        status_date=today
    ).first()
    
    # Get recent status history
    recent_statuses = DailyStatus.query.filter_by(
        vendor_id=vendor.id
    ).order_by(DailyStatus.status_date.desc()).limit(10).all()
    
    # Get pending mismatches
    pending_mismatches = MismatchRecord.query.filter_by(
        vendor_id=vendor.id,
        manager_approval=ApprovalStatus.PENDING
    ).all()
    
    # Check if today is weekend or holiday
    is_weekend = today.weekday() >= 5  # Saturday=5, Sunday=6
    is_holiday = Holiday.query.filter_by(holiday_date=today).first() is not None
    
    return render_template('vendor_dashboard.html', 
                         vendor=vendor,
                         manager=manager,
                         today_status=today_status,
                         recent_statuses=recent_statuses,
                         pending_mismatches=pending_mismatches,
                         is_weekend=is_weekend,
                         is_holiday=is_holiday,
                         today=today)
