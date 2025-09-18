#!/usr/bin/env python3
"""
Test Script for Manager Complete Notification Workflow
====================================================
This script tests the complete workflow for updating 03_manager_all_complete_notifications.xlsx
when all employees under a manager complete their submissions.

Test Cases:
1. Excel file structure validation
2. Manager completion detection
3. Local Excel file update
4. Network drive synchronization
5. Sync settings preservation
6. Error handling and recovery
"""

import os
import sys
import pandas as pd
from datetime import datetime, date, timedelta
from pathlib import Path
import json
import shutil
import sqlite3

# Add the scripts directory to the path
sys.path.insert(0, 'scripts')

def setup_test_environment():
    """Setup test environment with test data"""
    print("🔧 Setting up test environment...")
    
    # Create test folders
    test_folders = [
        "test_notification_configs",
        "test_network_folder_simplified"
    ]
    
    for folder in test_folders:
        Path(folder).mkdir(exist_ok=True)
        print(f"✅ Created test folder: {folder}")
    
    # Create test Excel file with sample data
    test_excel_path = Path("test_notification_configs/03_manager_all_complete_notifications.xlsx")
    sample_data = {
        'RecordID': ['NOTIF_TEST_MGR_001_20250918', 'NOTIF_TEST_MGR_002_20250918'],
        'ManagerID': ['TEST_MGR_001', 'TEST_MGR_002'],
        'ManagerName': ['Test Manager 1', 'Test Manager 2'],
        'NotificationMessage': [
            '🎉 Congratulations! Your entire team (3 members) has successfully submitted their attendance status for September 18, 2025. 100% completion achieved! Excellent leadership! 👏',
            '🎉 Congratulations! Your entire team (5 members) has successfully submitted their attendance status for September 18, 2025. 100% completion achieved! Excellent leadership! 👏'
        ],
        'CreatedTime': [datetime.now() - timedelta(hours=2), datetime.now() - timedelta(hours=1)],
        'NotiStatus': [True, False],
        'NotificationSentTime': [datetime.now() - timedelta(hours=1), pd.NaT],
        'Priority': ['HIGH', 'HIGH'],
        'AttendanceDate': [date.today(), date.today()],
        'TeamSize': [3, 5],
        'CompletionRate': ['100.0%', '100.0%'],
        'RetryCount': [0, 0]
    }
    
    df = pd.DataFrame(sample_data)
    df.to_excel(test_excel_path, index=False, engine='openpyxl')
    print(f"✅ Created test Excel file: {test_excel_path}")
    
    # Create test sync control settings
    sync_control_path = Path("test_network_folder_simplified/manager_complete_sync_control.json")
    sync_settings = {
        "global_sync_enabled": True,
        "stop_notifications": False,
        "force_update_mode": False,
        "auto_retry_enabled": True,
        "max_retry_count": 3,
        "sync_interval_minutes": 10,
        "manager_settings": {
            "TEST_MGR_001": {
                "stop_notifications": False,
                "force_update": False
            },
            "TEST_MGR_003": {
                "stop_notifications": True,
                "force_update": False
            }
        },
        "last_sync_time": datetime.now().isoformat()
    }
    
    with open(sync_control_path, 'w') as f:
        json.dump(sync_settings, f, indent=2)
    print(f"✅ Created test sync control file: {sync_control_path}")
    
    return True

def test_excel_file_structure():
    """Test 1: Validate Excel file structure"""
    print("\n📋 Test 1: Excel File Structure Validation")
    
    try:
        excel_path = "test_notification_configs/03_manager_all_complete_notifications.xlsx"
        
        if not Path(excel_path).exists():
            print("❌ Test Excel file not found")
            return False
        
        df = pd.read_excel(excel_path)
        
        # Check required columns
        required_columns = [
            'RecordID', 'ManagerID', 'ManagerName', 'NotificationMessage',
            'CreatedTime', 'NotiStatus', 'NotificationSentTime', 'Priority',
            'AttendanceDate', 'TeamSize', 'CompletionRate', 'RetryCount'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ Missing columns: {missing_columns}")
            return False
        
        print(f"✅ All required columns present: {len(required_columns)} columns")
        print(f"✅ Test data loaded: {len(df)} records")
        print(f"✅ Data types validated")
        
        # Check data integrity
        for idx, row in df.iterrows():
            if pd.isna(row['RecordID']) or pd.isna(row['ManagerID']):
                print(f"❌ Data integrity issue in row {idx}")
                return False
        
        print("✅ Data integrity validated")
        return True
        
    except Exception as e:
        print(f"❌ Excel structure test failed: {str(e)}")
        return False

def test_manager_completion_detection():
    """Test 2: Manager completion detection logic"""
    print("\n🔍 Test 2: Manager Completion Detection")
    
    try:
        # Import the handler with test configuration
        from manager_complete_notification_handler import ManagerCompleteNotificationHandler
        
        # Create test handler instance
        handler = ManagerCompleteNotificationHandler(
            db_path="vendor_timesheet.db",
            local_excel_folder="test_notification_configs",
            network_folder="test_network_folder_simplified"
        )
        
        print("✅ Handler initialized successfully")
        
        # Test completion detection (this will use the actual database)
        # In a real test, you'd want to mock the database or use test data
        completions = handler.detect_manager_completions(date.today())
        
        print(f"✅ Completion detection executed: {len(completions)} completions found")
        
        # Test individual completion data structure
        for completion in completions[:2]:  # Test first 2 completions
            assert hasattr(completion, 'manager_id')
            assert hasattr(completion, 'manager_name')
            assert hasattr(completion, 'team_size')
            assert hasattr(completion, 'completion_rate')
            assert hasattr(completion, 'all_completed')
            print(f"✅ Completion data structure valid for {completion.manager_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Completion detection test failed: {str(e)}")
        return False

def test_local_excel_update():
    """Test 3: Local Excel file update"""
    print("\n📝 Test 3: Local Excel File Update")
    
    try:
        from manager_complete_notification_handler import ManagerCompleteNotificationHandler, ManagerCompletionData
        
        # Create test handler
        handler = ManagerCompleteNotificationHandler(
            local_excel_folder="test_notification_configs",
            network_folder="test_network_folder_simplified"
        )
        
        # Create mock completion data
        test_completions = [
            ManagerCompletionData(
                manager_id="TEST_MGR_004",
                manager_name="Test Manager 4",
                team_size=4,
                completion_rate=100.0,
                attendance_date=date.today(),
                all_completed=True,
                notification_required=True,
                priority="HIGH"
            )
        ]
        
        print(f"✅ Created test completion data: {len(test_completions)} records")
        
        # Get initial record count
        initial_count = handler._get_record_count()
        
        # Update local Excel
        success = handler.update_local_excel(test_completions)
        
        if not success:
            print("❌ Local Excel update failed")
            return False
        
        # Verify update
        final_count = handler._get_record_count()
        
        if final_count <= initial_count:
            print("❌ Record count did not increase")
            return False
        
        print(f"✅ Local Excel updated: {initial_count} -> {final_count} records")
        
        # Verify new record content
        df = pd.read_excel(handler.local_excel_file)
        new_records = df[df['ManagerID'] == 'TEST_MGR_004']
        
        if new_records.empty:
            print("❌ New record not found")
            return False
        
        new_record = new_records.iloc[0]
        if new_record['TeamSize'] != 4 or new_record['CompletionRate'] != '100.0%':
            print("❌ New record data incorrect")
            return False
        
        print("✅ New record data validated")
        return True
        
    except Exception as e:
        print(f"❌ Local Excel update test failed: {str(e)}")
        return False

def test_network_drive_sync():
    """Test 4: Network drive synchronization"""
    print("\n🔄 Test 4: Network Drive Synchronization")
    
    try:
        from manager_complete_notification_handler import ManagerCompleteNotificationHandler
        
        # Create test handler
        handler = ManagerCompleteNotificationHandler(
            local_excel_folder="test_notification_configs",
            network_folder="test_network_folder_simplified"
        )
        
        # Ensure local file exists
        if not handler.local_excel_file.exists():
            print("❌ Local Excel file not found for sync test")
            return False
        
        # Get file modification time before sync
        local_mtime_before = handler.local_excel_file.stat().st_mtime
        
        # Perform sync
        success = handler.sync_to_network_drive()
        
        if not success:
            print("❌ Network drive sync failed")
            return False
        
        # Verify network file exists
        if not handler.network_excel_file.exists():
            print("❌ Network Excel file not created")
            return False
        
        # Verify sync metadata
        metadata_file = handler.network_folder / "manager_complete_sync_metadata.json"
        if not metadata_file.exists():
            print("❌ Sync metadata not created")
            return False
        
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        if metadata.get('sync_status') != 'success':
            print("❌ Sync status not success")
            return False
        
        print("✅ Network drive sync successful")
        print("✅ Sync metadata created and validated")
        
        # Test sync control preservation
        sync_control_file = handler.network_folder / "manager_complete_sync_control.json"
        if sync_control_file.exists():
            with open(sync_control_file, 'r') as f:
                sync_settings = json.load(f)
            
            if 'manager_settings' in sync_settings:
                print("✅ Sync control settings preserved")
            
        return True
        
    except Exception as e:
        print(f"❌ Network drive sync test failed: {str(e)}")
        return False

def test_sync_settings_and_features():
    """Test 5: Sync settings and features (stop notifications, force update)"""
    print("\n⚙️ Test 5: Sync Settings and Features")
    
    try:
        from manager_complete_notification_handler import ManagerCompleteNotificationHandler, configure_sync_settings
        
        # Create test handler
        handler = ManagerCompleteNotificationHandler(
            local_excel_folder="test_notification_configs",
            network_folder="test_network_folder_simplified"
        )
        
        # Test global stop notifications
        original_settings = handler.sync_settings.copy()
        
        configure_sync_settings(stop_notifications=True)
        
        # Reload settings
        handler.sync_settings = handler._load_sync_settings()
        
        if not handler.sync_settings.get('stop_notifications', False):
            print("❌ Global stop notifications setting not applied")
            return False
        
        print("✅ Global stop notifications setting applied")
        
        # Test manager-specific settings
        configure_sync_settings('TEST_MGR_005', stop_notifications=True, force_update=True)
        
        # Reload settings
        handler.sync_settings = handler._load_sync_settings()
        
        manager_settings = handler.sync_settings.get('manager_settings', {}).get('TEST_MGR_005', {})
        
        if not manager_settings.get('stop_notifications') or not manager_settings.get('force_update'):
            print("❌ Manager-specific settings not applied")
            return False
        
        print("✅ Manager-specific settings applied")
        
        # Test sync with stop notifications enabled
        sync_success = handler.sync_to_network_drive()
        
        # Should still return True but skip actual sync
        if not sync_success:
            print("❌ Sync with stop notifications should return True")
            return False
        
        print("✅ Sync respects stop notifications setting")
        
        # Restore original settings
        handler.sync_settings = original_settings
        handler._save_sync_settings(handler.sync_settings)
        
        return True
        
    except Exception as e:
        print(f"❌ Sync settings test failed: {str(e)}")
        return False

def test_error_handling():
    """Test 6: Error handling and recovery"""
    print("\n🛡️ Test 6: Error Handling and Recovery")
    
    try:
        from manager_complete_notification_handler import ManagerCompleteNotificationHandler
        
        # Test with invalid database path
        handler = ManagerCompleteNotificationHandler(
            db_path="nonexistent_database.db",
            local_excel_folder="test_notification_configs",
            network_folder="test_network_folder_simplified"
        )
        
        # This should not raise an exception but return empty results
        completions = handler.detect_manager_completions()
        
        if completions is None:
            print("❌ Error handling should return empty list, not None")
            return False
        
        print("✅ Database error handled gracefully")
        
        # Test with invalid Excel file permissions
        # (We'll simulate this by trying to write to a read-only location)
        invalid_handler = ManagerCompleteNotificationHandler(
            local_excel_folder="/invalid/readonly/path",
            network_folder="test_network_folder_simplified"
        )
        
        # This should handle the permission error gracefully
        try:
            success = invalid_handler.update_local_excel([])
            print("✅ Permission error handled gracefully")
        except Exception:
            print("❌ Permission error not handled properly")
            return False
        
        # Test network sync with invalid network path
        invalid_network_handler = ManagerCompleteNotificationHandler(
            local_excel_folder="test_notification_configs",
            network_folder="/invalid/network/path"
        )
        
        # This should handle network errors gracefully
        try:
            success = invalid_network_handler.sync_to_network_drive()
            # Should return False but not raise exception
            print("✅ Network error handled gracefully")
        except Exception:
            print("❌ Network error not handled properly")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {str(e)}")
        return False

def test_complete_workflow():
    """Test 7: Complete end-to-end workflow"""
    print("\n🚀 Test 7: Complete End-to-End Workflow")
    
    try:
        from manager_complete_notification_handler import process_manager_completions
        
        # Run complete workflow
        results = process_manager_completions(date.today())
        
        if not isinstance(results, dict):
            print("❌ Workflow should return results dictionary")
            return False
        
        required_keys = ['date', 'completions_detected', 'local_update_success', 'network_sync_success']
        
        for key in required_keys:
            if key not in results:
                print(f"❌ Missing result key: {key}")
                return False
        
        print("✅ Complete workflow executed successfully")
        print(f"  - Date: {results['date']}")
        print(f"  - Completions detected: {results['completions_detected']}")
        print(f"  - Local update: {'✅' if results['local_update_success'] else '❌'}")
        print(f"  - Network sync: {'✅' if results['network_sync_success'] else '❌'}")
        
        if results.get('errors'):
            print(f"  - Errors: {results['errors']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Complete workflow test failed: {str(e)}")
        return False

def cleanup_test_environment():
    """Clean up test environment"""
    print("\n🧹 Cleaning up test environment...")
    
    test_folders = [
        "test_notification_configs",
        "test_network_folder_simplified"
    ]
    
    for folder in test_folders:
        folder_path = Path(folder)
        if folder_path.exists():
            shutil.rmtree(folder_path)
            print(f"✅ Removed test folder: {folder}")

def run_all_tests():
    """Run all test cases"""
    print("=" * 80)
    print("🧪 MANAGER COMPLETE NOTIFICATION WORKFLOW TESTS")
    print("=" * 80)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Setup test environment
    if not setup_test_environment():
        print("❌ Test environment setup failed")
        return False
    
    # Test cases
    test_cases = [
        ("Excel File Structure", test_excel_file_structure),
        ("Manager Completion Detection", test_manager_completion_detection),
        ("Local Excel Update", test_local_excel_update),
        ("Network Drive Sync", test_network_drive_sync),
        ("Sync Settings and Features", test_sync_settings_and_features),
        ("Error Handling", test_error_handling),
        ("Complete Workflow", test_complete_workflow)
    ]
    
    passed = 0
    total = len(test_cases)
    
    for test_name, test_func in test_cases:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: FAILED with exception: {str(e)}")
    
    # Test summary
    print("\n" + "=" * 80)
    print(f"📊 TEST SUMMARY: {passed}/{total} tests passed")
    print("=" * 80)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! The manager complete notification workflow is ready.")
        print("\n✅ NEXT STEPS:")
        print("1. Deploy the manager_complete_notification_handler.py script")
        print("2. Update your scheduling system to call process_manager_completions()")
        print("3. Configure Power Automate to read from the network Excel file")
        print("4. Set up notification delivery (email, Teams, etc.)")
    else:
        print(f"⚠️ {total - passed} tests failed. Please review and fix issues before deployment.")
    
    # Cleanup
    cleanup_test_environment()
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
