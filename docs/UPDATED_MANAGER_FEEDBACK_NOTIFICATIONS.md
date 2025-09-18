# Manager Feedback Notifications - Updated
📋 **File**: `05_manager_feedback_notifications.xlsx`

## 📋 Purpose
Send comprehensive feedback from managers to vendors regarding:
- Status approvals, rejections, or corrections needed
- Billing correction notifications and confirmations  
- Time restriction warnings and reminders
- Manager action confirmations

## 👥 Recipients
- **Vendors**: Status feedback, billing corrections, time window notifications
- **Managers**: Confirmation of actions, restriction warnings

## 📱 Delivery Method
🟣 **Microsoft Teams** notifications

## ⏰ Trigger Conditions & Updated Logic

### 🔄 Status Management
- **Immediately** when manager approves/rejects daily status
- **Within 1 hour** of manager action
- **Includes** corrective actions if status rejected
- **Includes** manager comments and guidance
- **Includes** next steps clearly outlined

### 💰 Billing Correction Notifications (NEW)

#### 📅 **Time-Based Logic**:
- **Current Month**: Always correctable - no time restrictions
- **Previous Month**: Only correctable until 5th of next month
- **Older Records**: Not correctable

#### 🔔 **Notification Types**:

1. **Billing Corrected** (High Priority)
   - Sent to vendor when manager makes billing correction
   - Includes: date, old hours, new hours, reason
   - Example: "Manager has made billing correction for 2025-09-15: Hours updated from 7.5 to 8.0. Reason: Missing break time adjustment"

2. **Manager Correction Confirmation** (Medium Priority)
   - Sent to manager after successful billing correction
   - Confirms action was logged in audit trail
   - Example: "Billing correction recorded for EMP001 on 2025-09-15. Hours: 8.0. This correction has been logged in the audit trail."

3. **Correction Blocked** (Medium Priority)
   - Sent to manager when correction is blocked due to time restrictions
   - Example: "Unable to process billing correction for 2025-08-15. Previous month corrections are only allowed until the 5th of each month."

4. **Correction Window Reminder** (Medium Priority)
   - Sent to relevant users about upcoming deadlines
   - Example: "Reminder: Previous month billing corrections are available until the 5th. Currently 2 days remaining."

5. **Correction Window Closed** (Low Priority)
   - Sent when previous month correction window closes
   - Example: "Previous month billing correction window has closed. Current month corrections remain available."

### 📋 **Traditional Feedback** (Updated)

6. **Status Approved** (Medium Priority)
   - Positive feedback for approved daily status
   - Example: "Your daily status for 2025-09-17 has been approved by your manager. Great work!"

7. **Status Rejected** (High Priority)
   - Rejection with manager feedback and corrective actions
   - Example: "Your daily status for 2025-09-17 requires correction. Manager feedback: Hours seem inconsistent with project requirements. Please resubmit."

8. **Feedback Request** (High Priority)
   - Manager requests additional information
   - Example: "Your manager requests clarification on 2025-09-17 status. Please provide additional details or correct your submission."

## 🎯 **Smart Triggers**

### 📅 **Date-Based Triggers**:
- **1st-3rd of month**: Send correction window reminders
- **5th of month**: Send final day reminders
- **6th of month**: Send window closed notifications
- **Throughout month**: Process current month corrections normally

### 🚨 **Action-Based Triggers**:
- **Billing correction attempt**: Check date restrictions first
- **Successful correction**: Send confirmations to both manager and vendor
- **Blocked correction**: Send explanation to manager
- **Status approval/rejection**: Immediate notification with context

## 📊 **Notification Templates** (8 Types)

| Notification Type | Priority | Recipient | Purpose |
|------------------|----------|-----------|---------|
| Status Approved | Medium | Vendor | Positive reinforcement |
| Status Rejected | High | Vendor | Corrective action needed |
| Billing Corrected | High | Vendor | Correction notification |
| Correction Window Reminder | Medium | All | Deadline awareness |
| Correction Window Closed | Low | All | Window status update |
| Manager Correction Confirmation | Medium | Manager | Action confirmation |
| Correction Blocked | Medium | Manager | Restriction explanation |
| Feedback Request | High | Vendor | Clarification needed |

## 🔄 **Integration with Billing Logic**

### ✅ **Current Month Corrections**:
- No time restrictions
- Immediate notifications
- Full functionality maintained

### ⏰ **Previous Month Corrections**:
- Only allowed until 5th of next month
- Automatic blocking after 5th
- Clear explanatory notifications when blocked
- Reminders sent before deadline

### 🎯 **Business Benefits**:
1. **Transparency**: Users always know why corrections are blocked
2. **Proactive Communication**: Reminders before deadlines
3. **Audit Trail**: All actions confirmed via notifications  
4. **Compliance**: Clear documentation of time-based restrictions
5. **User Experience**: No confusion about when corrections are allowed

## 📋 **Message Variables**

All notification templates use dynamic variables:
- `{date}` - Specific date for the action
- `{manager_comments}` - Manager's feedback text
- `{old_hours}` / `{new_hours}` - Before/after hours for corrections
- `{correction_reason}` - Reason for billing correction
- `{vendor_id}` - Employee/vendor identifier
- `{corrected_hours}` - Final corrected hours value
- `{days_remaining}` - Days left in correction window

---

**Status**: ✅ **Updated and Active**
**Effective Date**: Immediate
**Impact**: Enhanced communication around billing corrections with time-based logic
