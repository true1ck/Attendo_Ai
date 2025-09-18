"""
Billing Correction Notifications Service
Handles dynamic notifications for billing correction actions
"""

from datetime import date, datetime
from backend.utils.helpers import send_notification


class BillingNotificationService:
    """Service to handle all billing correction related notifications"""
    
    @staticmethod
    def notify_successful_correction(manager_user_id, vendor_user_id, vendor_id, 
                                   correction_date, old_hours, new_hours, reason):
        """
        Send notifications for successful billing correction
        
        Args:
            manager_user_id (int): Manager's user ID
            vendor_user_id (int): Vendor's user ID  
            vendor_id (str): Vendor identifier
            correction_date (str): Date corrected (YYYY-MM-DD)
            old_hours (float): Previous hours value
            new_hours (float): New corrected hours
            reason (str): Reason for correction
        """
        try:
            # Notify vendor about the correction
            vendor_message = (
                f"Manager has made billing correction for {correction_date}: "
                f"Hours updated from {old_hours or 'N/A'} to {new_hours}. "
                f"Reason: {reason}"
            )
            send_notification(vendor_user_id, 'Billing Corrected', vendor_message)
            
            # Notify manager with confirmation
            manager_message = (
                f"Billing correction recorded for {vendor_id} on {correction_date}. "
                f"Hours: {new_hours}. This correction has been logged in the audit trail."
            )
            send_notification(manager_user_id, 'Manager Correction Confirmation', manager_message)
            
            print(f"✅ Sent billing correction notifications for {vendor_id} on {correction_date}")
            
        except Exception as e:
            print(f"❌ Error sending billing correction notifications: {e}")
            # Don't raise - notifications shouldn't break the correction process
    
    
    @staticmethod
    def notify_blocked_correction(manager_user_id, correction_date, reason):
        """
        Send notification when correction is blocked
        
        Args:
            manager_user_id (int): Manager's user ID
            correction_date (str): Date attempted (YYYY-MM-DD)
            reason (str): Reason why blocked
        """
        try:
            blocked_message = f"Unable to process billing correction for {correction_date}. {reason}"
            send_notification(manager_user_id, 'Correction Blocked', blocked_message)
            
            print(f"⚠️ Sent blocked correction notification for {correction_date}")
            
        except Exception as e:
            print(f"❌ Error sending blocked correction notification: {e}")
    
    
    @staticmethod
    def notify_correction_window_status(user_id, status_type, additional_info=None):
        """
        Send correction window status notifications
        
        Args:
            user_id (int): User ID to notify
            status_type (str): Type of status ('opened', 'reminder', 'final', 'closed')
            additional_info (dict): Additional information for dynamic messages
        """
        try:
            today = date.today()
            
            if status_type == 'opened':
                days_remaining = additional_info.get('days_remaining', 5)
                message = (
                    f"Billing correction window is now open! "
                    f"You have {days_remaining} days to correct previous month records."
                )
                notification_type = 'Correction Window Opened'
                
            elif status_type == 'reminder':
                days_remaining = additional_info.get('days_remaining', 0)
                if days_remaining <= 1:
                    message = f"Urgent: Only {days_remaining} day remaining for previous month billing corrections!"
                else:
                    message = f"Reminder: {days_remaining} days remaining for previous month billing corrections."
                notification_type = 'Correction Window Reminder'
                
            elif status_type == 'final':
                message = (
                    "🚨 FINAL DAY: Previous month billing correction window closes today! "
                    "This is your last chance to make corrections."
                )
                notification_type = 'Final Correction Day'
                
            elif status_type == 'closed':
                message = (
                    "Previous month billing correction window has closed. "
                    "Current month corrections remain available throughout the month."
                )
                notification_type = 'Correction Window Closed'
                
            else:
                print(f"⚠️ Unknown notification status type: {status_type}")
                return
            
            send_notification(user_id, notification_type, message)
            print(f"📅 Sent {status_type} notification to user {user_id}")
            
        except Exception as e:
            print(f"❌ Error sending window status notification: {e}")


# Convenience functions for direct use in routes
def send_correction_success_notifications(manager_user_id, vendor_user_id, vendor_id, 
                                        correction_date, old_hours, new_hours, reason):
    """Convenience function for successful correction notifications"""
    BillingNotificationService.notify_successful_correction(
        manager_user_id, vendor_user_id, vendor_id, 
        correction_date, old_hours, new_hours, reason
    )


def send_correction_blocked_notification(manager_user_id, correction_date, reason):
    """Convenience function for blocked correction notifications"""
    BillingNotificationService.notify_blocked_correction(
        manager_user_id, correction_date, reason
    )


def send_window_status_notification(user_id, status_type, **kwargs):
    """Convenience function for window status notifications"""
    BillingNotificationService.notify_correction_window_status(
        user_id, status_type, kwargs
    )
