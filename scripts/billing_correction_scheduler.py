#!/usr/bin/env python3
"""
Billing Correction Reminder Scheduler
Sends automated reminders about billing correction deadlines
"""

import sys
import os
from datetime import date, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models import Manager, Vendor, User, UserRole
from utils import send_notification
from backend.utils.helpers import can_edit_billing_corrections


def send_billing_correction_reminders():
    """
    Send reminders about billing correction deadlines
    This function should be called daily by the scheduler
    """
    try:
        today = date.today()
        current_day = today.day
        
        print(f"🔔 Checking billing correction reminders for {today}")
        
        # Only send reminders during the first 5 days of the month
        if current_day > 5:
            print("📅 Past correction window - no reminders needed")
            return
        
        # Get correction status
        can_edit, message, allowed_dates = can_edit_billing_corrections()
        
        if not allowed_dates.get('can_edit_previous_month'):
            print("📅 Previous month corrections not available")
            return
            
        # Calculate days remaining for previous month corrections
        deadline_date = date(today.year, today.month, 5)
        days_remaining = (deadline_date - today).days
        
        # Send reminders based on days remaining
        if current_day == 1:
            # First day reminder
            send_correction_window_opened_notifications(days_remaining)
        elif current_day in [3, 4]:  # 3rd and 4th day reminders
            send_correction_deadline_reminders(days_remaining)
        elif current_day == 5:
            # Last day urgent reminder
            send_final_day_reminders()
            
    except Exception as e:
        print(f"❌ Error in billing correction reminder scheduler: {e}")


def send_correction_window_opened_notifications(days_remaining):
    """Send notifications when correction window opens (1st of month)"""
    try:
        # Get all managers
        managers = Manager.query.join(User).filter(User.is_active == True).all()
        
        for manager in managers:
            if manager.user_account:
                message = f"Billing correction window is now open! You have {days_remaining + 1} days to correct previous month records for your team members."
                send_notification(manager.user_account.id, 'Correction Window Opened', message)
                
        print(f"✅ Sent {len(managers)} correction window opened notifications")
        
    except Exception as e:
        print(f"❌ Error sending window opened notifications: {e}")


def send_correction_deadline_reminders(days_remaining):
    """Send deadline reminders (3rd and 4th day)"""
    try:
        # Get all managers with team members
        managers = Manager.query.join(User).filter(User.is_active == True).all()
        active_managers = [m for m in managers if m.team_vendors.count() > 0]
        
        for manager in active_managers:
            if manager.user_account:
                if days_remaining == 2:
                    message = f"Reminder: {days_remaining} days remaining to correct previous month billing records for your team."
                elif days_remaining == 1:
                    message = f"Urgent: Only {days_remaining} day remaining for previous month billing corrections!"
                else:
                    message = f"Reminder: {days_remaining} days remaining for previous month billing corrections."
                    
                send_notification(manager.user_account.id, 'Correction Window Reminder', message)
                
        print(f"✅ Sent {len(active_managers)} correction deadline reminders ({days_remaining} days remaining)")
        
    except Exception as e:
        print(f"❌ Error sending deadline reminders: {e}")


def send_final_day_reminders():
    """Send urgent final day reminders (5th of month)"""
    try:
        # Get all managers with team members
        managers = Manager.query.join(User).filter(User.is_active == True).all()
        active_managers = [m for m in managers if m.team_vendors.count() > 0]
        
        for manager in active_managers:
            if manager.user_account:
                message = "🚨 FINAL DAY: Previous month billing correction window closes today! This is your last chance to make corrections."
                send_notification(manager.user_account.id, 'Final Correction Day', message)
                
        print(f"🚨 Sent {len(active_managers)} final day urgent reminders")
        
    except Exception as e:
        print(f"❌ Error sending final day reminders: {e}")


def send_correction_window_closed_notifications():
    """Send notifications when correction window closes (6th of month)"""
    try:
        today = date.today()
        if today.day != 6:
            return
            
        # Get all managers
        managers = Manager.query.join(User).filter(User.is_active == True).all()
        
        for manager in managers:
            if manager.user_account:
                message = "Previous month billing correction window has closed. Current month corrections remain available throughout the month."
                send_notification(manager.user_account.id, 'Correction Window Closed', message)
                
        print(f"📅 Sent {len(managers)} correction window closed notifications")
        
    except Exception as e:
        print(f"❌ Error sending window closed notifications: {e}")


def schedule_daily_billing_reminders(app):
    """
    Schedule daily billing correction reminders
    This should be integrated with the existing scheduler service
    """
    try:
        with app.app_context():
            today = date.today()
            current_day = today.day
            
            # Run appropriate reminder based on day of month
            if current_day <= 5:
                send_billing_correction_reminders()
            elif current_day == 6:
                send_correction_window_closed_notifications()
                
    except Exception as e:
        print(f"❌ Error in daily billing reminder scheduler: {e}")


if __name__ == "__main__":
    # For testing purposes
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from app import app
    
    print("🔔 Testing Billing Correction Reminder System")
    print("=" * 50)
    
    with app.app_context():
        send_billing_correction_reminders()
        
    print("✅ Test completed")
