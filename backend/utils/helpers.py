"""
Helper Utility Functions
General utility functions used across the application
"""

import json
from datetime import datetime
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
