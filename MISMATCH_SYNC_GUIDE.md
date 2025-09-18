# Mismatch Notifications Real-time Sync Guide

## 📋 Overview

The `04_mismatch_notifications.xlsx` file now has **real-time sync functionality** that automatically detects attendance mismatches, updates local Excel files, and syncs to the network drive with proper table formatting for Power Automate integration.

## 🚨 Key Features

### ✅ Real-time Mismatch Detection:
- **Automatic Detection**: Scans for mismatches between web status and swipe records
- **Smart Analysis**: Identifies 5 types of mismatches with severity levels
- **Instant Updates**: Updates Excel files immediately when mismatches are found
- **Duplicate Prevention**: Avoids sending duplicate notifications

### 📊 Mismatch Types Detected:
1. **NO_WEB_STATUS_BUT_SWIPED** (HIGH) - Employee swiped but didn't submit web status
2. **WFH_BUT_SWIPED** (HIGH) - Marked Work From Home but has swipe records
3. **ON_LEAVE_BUT_SWIPED** (HIGH) - Marked On Leave but has swipe records  
4. **OFFICE_BUT_NO_SWIPE** (HIGH) - Marked In Office but has no swipe records
5. **FULL_DAY_BUT_PARTIAL_SWIPE** (MEDIUM) - Marked Full Day but partial swipe

### 🎨 Excel Table Features:
- **Table Name**: `MismatchNotifications`
- **Style**: `TableStyleMedium12` (Red/orange alert theme)
- **Auto-sized Columns**: Automatically adjusts for readability
- **19 Columns**: Comprehensive mismatch data tracking
- **Power Automate Ready**: Proper table format for automation

## 🚀 How to Use

### Command Line Interface:
```bash
# Process real-time mismatches
python scripts/mismatch_notification_handler.py --action process

# Check pending notifications
python scripts/mismatch_notification_handler.py --action pending

# Check system status
python scripts/mismatch_notification_handler.py --action status

# Force sync to network
python scripts/mismatch_notification_handler.py --action sync

# Format existing file as table
python scripts/mismatch_notification_handler.py --action format-table

# Configure employee-specific settings
python scripts/mismatch_notification_handler.py --employee-id EMP001 --stop-notifications
```

### Verification:
```bash
# Run comprehensive system verification
python verify_mismatch_sync.py
```

## 📁 File Locations

### Local Files:
- `notification_configs/04_mismatch_notifications.xlsx`

### Network Files:
- `network_folder_simplified/04_mismatch_notifications.xlsx`
- `network_folder_simplified/mismatch_sync_control.json`
- `network_folder_simplified/mismatch_sync_metadata.json`
- `network_folder_simplified/notification_context.json`

## 🔧 Integration Points

### Daily Processing:
- **Integrated** with `daily_excel_updater.py`
- **Automatic** processing during daily reset
- **Real-time** checks on vendor status updates

### Power Automate Configuration:
```odata
# Get pending mismatch notifications
NotificationSent eq false

# Filter by severity
NotificationSent eq false and Severity eq 'HIGH'

# Filter by mismatch type
MismatchType eq 'OFFICE_BUT_NO_SWIPE'

# Filter by today's date
MismatchDate eq formatDateTime(utcnow(),'yyyy-MM-dd')
```

## 📊 Excel Columns Structure

| Column | Description | Example |
|--------|-------------|---------|
| `RecordID` | Unique identifier | MISMATCH_EMP001_20250919_141530 |
| `EmployeeID` | Employee identifier | EMP001 |
| `ContactEmail` | Employee email | employee@company.com |
| `EmployeeName` | Employee full name | John Smith |
| `MismatchDate` | Date of mismatch | 2025-09-19 |
| `WebStatus` | Status submitted on web | IN_OFFICE_FULL |
| `SwipeStatus` | Detected swipe status | NO_SWIPE |
| `MismatchType` | Type of mismatch | OFFICE_BUT_NO_SWIPE |
| `Message` | Ready-to-send notification | 🚨 Attendance Mismatch Alert... |
| `NotificationType` | Always MISMATCH_ALERT | MISMATCH_ALERT |
| `Priority` | HIGH/MEDIUM/LOW | HIGH |
| `Severity` | HIGH/MEDIUM/LOW | HIGH |
| `CreatedTime` | When record was created | 2025-09-19 14:15:30 |
| `NotificationSent` | true/false | false |
| `NotificationSentTime` | When sent | NULL or timestamp |
| `ExplanationRequired` | true/false | true |
| `ManagerID` | Manager identifier | MGR001 |
| `ManagerEmail` | Manager email | manager@company.com |
| `RetryCount` | Retry attempts | 0 |

## 🔄 Sync Settings

### Global Settings:
```json
{
  "global_sync_enabled": true,
  "stop_notifications": false,
  "force_update_mode": false,
  "sync_interval_minutes": 5,
  "mismatch_detection_enabled": true
}
```

### Employee-Specific Settings:
```json
{
  "employee_settings": {
    "EMP001": {
      "stop_notifications": false,
      "force_update": false
    }
  }
}
```

## 🚨 Notification Messages Examples

### Office But No Swipe:
> 🚨 Attendance Mismatch Alert - You marked In Office but have no swipe records for September 19, 2025. Web Status: In Office Full, Swipe Status: No Swipe. Please provide an explanation.

### WFH But Swiped:
> 🚨 Attendance Mismatch Alert - You marked Work From Home but have swipe records for September 19, 2025. Web Status: Work From Home, Swipe Status: Full Day Office. Please provide an explanation.

## 📊 Current System Status

✅ **Real-time Detection**: ACTIVE  
✅ **Local Updates**: WORKING  
✅ **Network Sync**: WORKING  
✅ **Table Formatting**: CORRECT  
✅ **Power Automate Ready**: YES  

### Live Statistics:
- **Total Records**: 8 (as of last verification)
- **Pending Notifications**: 2
- **Sync Status**: Enabled
- **Last Detection**: Active (found 1 new mismatch)

## 🔍 Troubleshooting

### Common Issues:

#### No Mismatches Detected:
- Check database connection
- Verify daily_statuses and swipe_records tables have data
- Ensure employees have submitted web status

#### Sync Not Working:
```bash
# Check sync settings
python scripts/mismatch_notification_handler.py --action status

# Force sync
python scripts/mismatch_notification_handler.py --action sync
```

#### Table Format Issues:
```bash
# Re-format as table
python scripts/mismatch_notification_handler.py --action format-table
```

#### Power Automate Connection Issues:
1. Verify table name is exactly: `MismatchNotifications`
2. Check file path in notification context
3. Refresh Excel connection in Power Automate
4. Ensure network drive is accessible

## 🚀 Next Steps

### For Power Automate:
1. **Create Flow**: Use "List rows present in a table" action
2. **Table Reference**: `MismatchNotifications`
3. **Filter**: `NotificationSent eq false`
4. **Frequency**: Every 5-10 minutes for real-time alerts

### For Notification Delivery:
1. **Email**: Use notification message directly
2. **Teams**: Format as adaptive card
3. **SMS**: Extract key details for short message
4. **Dashboard**: Show pending count and severity

### For Monitoring:
1. **Check logs**: Review sync metadata regularly
2. **Monitor counts**: Track pending notifications
3. **Test scenarios**: Verify different mismatch types
4. **Performance**: Ensure 5-minute sync intervals work

---

**🎉 Your mismatch notification system is now fully operational with real-time sync capabilities!**

For support or issues, check the verification script output or review the sync logs in the network folder.
