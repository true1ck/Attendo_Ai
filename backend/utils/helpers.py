"""
Helper Utility Functions
General utility functions used across the application
"""

import json
from datetime import datetime, date, timedelta
from flask import request
from backend.models import AuditLog
from backend.extensions import db


def create_audit_log(user_id, action, table_name, record_id=None, old_values=None, new_values=None):
    """Create an audit log entry"""
    try:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            table_name=table_name,
            record_id=record_id,
            old_values=json.dumps(old_values) if old_values else None,
            new_values=json.dumps(new_values) if new_values else None,
            ip_address=request.remote_addr if request else None,
            user_agent=request.user_agent.string if request else None
        )
        db.session.add(audit_log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating audit log: {str(e)}")


def send_notification(recipient_id, notification_type, message):
    """Send notification to user and log it"""
    from backend.models import NotificationLog
    try:
        notification = NotificationLog(
            recipient_id=recipient_id,
            notification_type=notification_type,
            message=message
        )
        db.session.add(notification)
        db.session.commit()
        
        # Here you could integrate with actual Teams API
        # For demo, we'll just log it
        print(f"Notification sent to user {recipient_id}: {message}")
        
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error sending notification: {str(e)}")
        return False


def can_edit_billing_corrections():
    """Check if billing corrections are allowed based on current date.
    
    Billing corrections are always allowed for the current month.
    Previous month corrections are only allowed until the 5th of the current month.
    
    Returns:
        tuple: (is_allowed: bool, message: str, allowed_dates: dict)
    """
    today = date.today()
    current_day = today.day
    
    # Calculate current month range
    first_day_current_month = date(today.year, today.month, 1)
    
    # Calculate the previous month date range
    if today.month == 1:
        prev_month = 12
        prev_year = today.year - 1
    else:
        prev_month = today.month - 1
        prev_year = today.year
    
    # Get first and last day of previous month
    first_day_prev_month = date(prev_year, prev_month, 1)
    
    # Get last day of previous month
    if prev_month == 12:
        next_month_year = prev_year + 1
        next_month_num = 1
    else:
        next_month_year = prev_year
        next_month_num = prev_month + 1
    
    last_day_prev_month = date(next_month_year, next_month_num, 1) - timedelta(days=1)
    
    # Calculate allowed date ranges
    if current_day <= 5:
        # Can edit both current and previous month
        min_date = first_day_prev_month
        max_date = today  # Don't allow future dates
        message = f"You can make billing corrections for {first_day_prev_month.strftime('%B %Y')} and {first_day_current_month.strftime('%B %Y')} until {date(today.year, today.month, 5).strftime('%B %d, %Y')} (previous month deadline)."
    else:
        # Can only edit current month
        min_date = first_day_current_month
        max_date = today  # Don't allow future dates
        message = f"You can make billing corrections for {first_day_current_month.strftime('%B %Y')} only. Previous month corrections were available until {date(today.year, today.month, 5).strftime('%B %d, %Y')}."
    
    return (
        True,  # Always allow corrections (but with date restrictions)
        message,
        {
            'min_date': min_date.isoformat(),
            'max_date': max_date.isoformat(),
            'current_month_start': first_day_current_month.isoformat(),
            'prev_month_start': first_day_prev_month.isoformat(),
            'prev_month_end': last_day_prev_month.isoformat(),
            'can_edit_previous_month': current_day <= 5
        }
    )


def validate_billing_correction_date(correction_date_str):
    """Validate if a specific date can be corrected based on current date rules.
    
    Args:
        correction_date_str (str): Date string in YYYY-MM-DD format
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    try:
        correction_date = datetime.strptime(correction_date_str, '%Y-%m-%d').date()
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD format."
    
    today = date.today()
    
    # Don't allow future dates
    if correction_date > today:
        return False, "You cannot correct future dates."
    
    # Get allowed date ranges
    can_edit, general_message, allowed_dates = can_edit_billing_corrections()
    
    # Check if the specific date is within the allowed range
    min_date = datetime.fromisoformat(allowed_dates['min_date']).date()
    max_date = datetime.fromisoformat(allowed_dates['max_date']).date()
    
    if correction_date < min_date:
        if allowed_dates.get('can_edit_previous_month'):
            return False, f"You can only correct dates from {min_date.strftime('%B %Y')} onwards."
        else:
            current_month_start = datetime.fromisoformat(allowed_dates['current_month_start']).date()
            return False, f"You can only correct dates from {current_month_start.strftime('%B %Y')} onwards. Previous month corrections were available until the 5th."
    
    if correction_date > max_date:
        return False, f"You can only correct dates up to {max_date.strftime('%B %d, %Y')}."
    
    # Additional check for previous month after 5th
    if not allowed_dates.get('can_edit_previous_month'):
        current_month_start = datetime.fromisoformat(allowed_dates['current_month_start']).date()
        if correction_date < current_month_start:
            return False, f"Previous month corrections are no longer allowed after the 5th. You can only correct {current_month_start.strftime('%B %Y')} dates."
    
    return True, "Date is valid for correction."
