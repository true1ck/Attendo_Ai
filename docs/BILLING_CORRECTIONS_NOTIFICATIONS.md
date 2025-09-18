# Billing Corrections Dynamic Notifications

## Overview
Dynamic notification system for billing correction actions with time-based restrictions.

## Implementation Files

### 📁 Backend Services
- **`backend/services/billing_notifications.py`**: Main notification service
- **`backend/utils/helpers.py`**: Date validation functions (updated)

### 📁 Scripts  
- **`scripts/billing_correction_scheduler.py`**: Scheduled reminder system

### 📁 Routes
- **`backend/routes/manager_routes.py`**: Backend route with notifications (updated)
- **`app.py`**: Main route with notifications (updated)

### 📁 Notification Config
- **`notification_configs/05_manager_feedback_notifications.xlsx`**: Templates (updated)

## Notification Triggers

### 🔄 **Real-Time (Immediate)**
1. **Successful Correction**
   - Vendor: "Manager has made billing correction for {date}..."
   - Manager: "Billing correction recorded for {vendor}..."

2. **Blocked Correction**
   - Manager: "Unable to process billing correction for {date}..."

### ⏰ **Scheduled (Daily)**
- **1st of Month**: Window opened notifications
- **3rd-4th**: Deadline reminders  
- **5th**: Final day warnings
- **6th**: Window closed notifications

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌────────────────┐
│   Manager UI    │ -> │   Route Handler  │ -> │  Notification  │
│  (Correction)   │    │  (Validation)    │    │    Service     │
└─────────────────┘    └──────────────────┘    └────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌────────────────┐
                       │   Audit Trail    │    │  Teams/Excel   │
                       │    (Logging)     │    │ (Notifications)│
                       └──────────────────┘    └────────────────┘
```

## Usage

### In Routes
```python
from backend.services.billing_notifications import send_correction_success_notifications

# After successful correction
send_correction_success_notifications(
    manager_user_id=current_user.id,
    vendor_user_id=vendor.user_id,
    vendor_id=vendor_id,
    correction_date=date_str,
    old_hours=old_hours,
    new_hours=corrected_hours,
    reason=reason
)
```

### In Scheduler
```python
from scripts.billing_correction_scheduler import schedule_daily_billing_reminders

# Daily at 9 AM
schedule.every().day.at("09:00").do(schedule_daily_billing_reminders, app)
```

## Configuration

All notification templates are stored in:
`notification_configs/05_manager_feedback_notifications.xlsx`

8 notification types covering all scenarios with dynamic variables.

## Error Handling

- Notifications wrapped in try-catch blocks
- Failed notifications don't break correction process  
- Errors logged for debugging
- System continues if notification service unavailable

## Status: ✅ Active
Real-time notifications implemented and working.
Scheduled reminders ready for scheduler integration.
