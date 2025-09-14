"""
Database Utilities
Functions for database operations and data management
"""

from datetime import datetime, date, timedelta
from backend.models import Holiday, SystemConfiguration
from backend.extensions import db


def get_system_config(key, default_value=None):
    """Get system configuration value"""
    config = SystemConfiguration.query.filter_by(key=key).first()
    return config.value if config else default_value


def set_system_config(key, value, description, user_id):
    """Set system configuration value"""
    from backend.utils.helpers import create_audit_log
    
    config = SystemConfiguration.query.filter_by(key=key).first()
    
    if config:
        old_value = config.value
        config.value = value
        config.updated_by = user_id
        config.updated_at = datetime.utcnow()
        
        create_audit_log(user_id, 'UPDATE', 'system_configurations', config.id,
                       {'value': old_value}, {'value': value})
    else:
        config = SystemConfiguration(
            key=key,
            value=value,
            description=description,
            updated_by=user_id
        )
        db.session.add(config)
        
        create_audit_log(user_id, 'CREATE', 'system_configurations', None, {},
                       {'key': key, 'value': value, 'description': description})
    
    db.session.commit()


def calculate_working_days(start_date, end_date):
    """Calculate working days between two dates (excluding weekends and holidays)"""
    working_days = 0
    current_date = start_date
    
    # Get all holidays in the date range
    holidays = Holiday.query.filter(
        Holiday.holiday_date >= start_date,
        Holiday.holiday_date <= end_date
    ).all()
    holiday_dates = {h.holiday_date for h in holidays}
    
    while current_date <= end_date:
        # Skip weekends (Saturday=5, Sunday=6)
        if current_date.weekday() < 5 and current_date not in holiday_dates:
            working_days += 1
        current_date += timedelta(days=1)
    
    return working_days


def check_late_submissions():
    """Check for vendors who haven't submitted today's status"""
    from backend.models import User, Vendor, DailyStatus
    
    today = date.today()
    
    # Skip weekends and holidays
    if today.weekday() >= 5:  # Weekend
        return []
    
    if Holiday.query.filter_by(holiday_date=today).first():  # Holiday
        return []
    
    # Get all active vendors
    vendors = Vendor.query.join(User).filter(User.is_active == True).all()
    late_vendors = []
    
    for vendor in vendors:
        # Check if status submitted for today
        status = DailyStatus.query.filter_by(
            vendor_id=vendor.id,
            status_date=today
        ).first()
        
        if not status:
            late_vendors.append(vendor)
    
    return late_vendors
