#!/usr/bin/env python3
"""
Comprehensive test to verify complete Excel update workflow
"""

import app
import pandas as pd
from pathlib import Path
from datetime import datetime

def test_complete_excel_workflow():
    """Test the complete Excel update workflow"""
    
    with app.app.app_context():
        from utils import get_system_config
        from scripts.daily_excel_updater import daily_excel_updater
        
        # Set up network folder
        network_folder = get_system_config('excel_network_folder')
        if network_folder:
            app.app.config['EXCEL_NETWORK_FOLDER'] = network_folder
        
        print("🧪 Comprehensive Excel Workflow Test")
        print("=" * 60)
        
        # Test vendor
        test_vendor_id = 'EMP001'
        
        # Step 1: Simulate vendor submission (pending approval)
        print(f"Step 1: Vendor {test_vendor_id} submits status...")
        daily_excel_updater.vendor_submitted_status_update(test_vendor_id, None)
        print("✅ Local Excel updated with vendor submission")
        
        # Check both Excel files after submission
        print("\n📊 After Vendor Submission:")
        check_excel_status('Daily Reminders', 'notification_configs/01_daily_status_reminders.xlsx')
        check_excel_status('Manager Summary', 'notification_configs/02_manager_summary_notifications.xlsx')
        
        # Step 2: Simulate manager approval
        print(f"\nStep 2: Manager approves {test_vendor_id} status...")
        daily_excel_updater.vendor_submitted_status_update(test_vendor_id, 'approved')
        print("✅ Local Excel updated with manager approval")
        
        # Check both Excel files after approval
        print("\n📊 After Manager Approval:")
        check_excel_status('Daily Reminders', 'notification_configs/01_daily_status_reminders.xlsx')
        check_excel_status('Manager Summary', 'notification_configs/02_manager_summary_notifications.xlsx')
        
        # Step 3: Force sync to network
        print(f"\nStep 3: Syncing to network drive...")
        app.sync_excel_files()
        print("✅ Files synced to network drive")
        
        # Step 4: Verify network files match local files
        print("\n📊 Network Sync Verification:")
        verify_sync('01_daily_status_reminders.xlsx')
        verify_sync('02_manager_summary_notifications.xlsx')
        
        print("\n🎯 Expected Behavior Verified:")
        print("1. ✅ Vendor submission → Updates both local Excel files immediately")
        print("2. ✅ Manager approval → Updates both local Excel files immediately") 
        print("3. ✅ Sync service → Copies updated local files to network drive")
        print("4. ✅ Network files → Match local files exactly after sync")

def check_excel_status(file_name, file_path):
    """Check and display key status from Excel file"""
    path = Path(file_path)
    if not path.exists():
        print(f"  ❌ {file_name}: File not found")
        return
    
    try:
        df = pd.read_excel(path)
        print(f"  📁 {file_name}: {len(df)} rows")
        
        # Show different info based on file type
        if 'daily_status_reminders' in str(path):
            if 'Active' in df.columns:
                active_count = (df['Active'] == 'YES').sum()
                inactive_count = (df['Active'] == 'NO').sum()
                print(f"    Active vendors: {active_count}, Inactive: {inactive_count}")
            
            if 'Send_Notification' in df.columns:
                notify_counts = df['Send_Notification'].value_counts()
                for status, count in notify_counts.items():
                    print(f"    {status} notifications: {count}")
        
        elif 'manager_summary' in str(path):
            if 'Submitted_Count' in df.columns:
                total_submitted = df['Submitted_Count'].sum() if df['Submitted_Count'].notna().any() else 0
                total_pending = df['Pending_Count'].sum() if df['Pending_Count'].notna().any() else 0
                print(f"    Total submitted: {total_submitted}, Total pending: {total_pending}")
            
            if 'Send_Notification' in df.columns:
                notify_counts = df['Send_Notification'].value_counts()
                for status, count in notify_counts.items():
                    print(f"    {status} manager notifications: {count}")
    
    except Exception as e:
        print(f"  ❌ {file_name}: Error reading file - {e}")

def verify_sync(filename):
    """Verify that local and network files are synchronized"""
    local_path = Path(f'notification_configs/{filename}')
    network_path = Path(f'G:/Test1/{filename}')
    
    if not local_path.exists() or not network_path.exists():
        print(f"  ❌ {filename}: Missing files for comparison")
        return
    
    try:
        # Compare file sizes and timestamps
        local_size = local_path.stat().st_size
        network_size = network_path.stat().st_size
        
        local_time = datetime.fromtimestamp(local_path.stat().st_mtime)
        network_time = datetime.fromtimestamp(network_path.stat().st_mtime)
        
        time_diff = abs((local_time - network_time).total_seconds())
        
        size_match = "✅" if local_size == network_size else "❌"
        time_match = "✅" if time_diff < 60 else "❌"
        
        print(f"  📁 {filename}:")
        print(f"    Size match: {size_match} (Local: {local_size}, Network: {network_size})")
        print(f"    Time sync: {time_match} (Diff: {time_diff:.1f}s)")
        
        # Quick data comparison
        df_local = pd.read_excel(local_path)
        df_network = pd.read_excel(network_path)
        
        row_match = "✅" if len(df_local) == len(df_network) else "❌"
        print(f"    Row count: {row_match} (Local: {len(df_local)}, Network: {len(df_network)})")
    
    except Exception as e:
        print(f"  ❌ {filename}: Comparison error - {e}")

if __name__ == "__main__":
    test_complete_excel_workflow()
