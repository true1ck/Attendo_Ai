"""
Custom Assertion Functions
==========================

Custom assertion functions for validating objects and responses in tests.
"""

import os
import sys
from typing import Any, Dict, List, Optional
from datetime import date, time, datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from models import User, UserRole, Vendor, Manager, DailyStatus, AttendanceStatus, ApprovalStatus


def assert_user_valid(user: User, expected_values: Optional[Dict[str, Any]] = None):
    """Assert that a User object is valid and matches expected values."""
    # Basic validation
    assert user is not None, "User should not be None"
    assert user.id is not None, "User should have an ID"
    assert user.username is not None, "User should have a username"
    assert user.email is not None, "User should have an email"
    assert user.password_hash is not None, "User should have a password hash"
    assert user.role is not None, "User should have a role"
    assert isinstance(user.role, UserRole), "User role should be a UserRole enum"
    assert user.created_at is not None, "User should have a created_at timestamp"
    
    # Email format validation
    assert "@" in user.email, "Email should contain @ symbol"
    assert "." in user.email, "Email should contain a domain"
    
    # Role validation
    assert user.role in [UserRole.VENDOR, UserRole.MANAGER, UserRole.ADMIN], \
        f"Invalid user role: {user.role}"
    
    # Expected values validation
    if expected_values:
        for key, expected_value in expected_values.items():
            actual_value = getattr(user, key, None)
            assert actual_value == expected_value, \
                f"Expected {key}={expected_value}, got {actual_value}"


def assert_vendor_valid(vendor: Vendor, expected_values: Optional[Dict[str, Any]] = None):
    """Assert that a Vendor object is valid and matches expected values."""
    # Basic validation
    assert vendor is not None, "Vendor should not be None"
    assert vendor.id is not None, "Vendor should have an ID"
    assert vendor.user_id is not None, "Vendor should have a user_id"
    assert vendor.vendor_id is not None, "Vendor should have a vendor_id"
    assert vendor.full_name is not None, "Vendor should have a full_name"
    assert vendor.department is not None, "Vendor should have a department"
    assert vendor.company is not None, "Vendor should have a company"
    assert vendor.band is not None, "Vendor should have a band"
    assert vendor.location is not None, "Vendor should have a location"
    assert vendor.created_at is not None, "Vendor should have a created_at timestamp"
    
    # Format validations
    assert len(vendor.vendor_id.strip()) > 0, "Vendor ID should not be empty"
    assert len(vendor.full_name.strip()) > 0, "Full name should not be empty"
    assert len(vendor.department.strip()) > 0, "Department should not be empty"
    assert len(vendor.company.strip()) > 0, "Company should not be empty"
    assert len(vendor.band.strip()) > 0, "Band should not be empty"
    assert len(vendor.location.strip()) > 0, "Location should not be empty"
    
    # Expected values validation
    if expected_values:
        for key, expected_value in expected_values.items():
            actual_value = getattr(vendor, key, None)
            assert actual_value == expected_value, \
                f"Expected {key}={expected_value}, got {actual_value}"


def assert_manager_valid(manager: Manager, expected_values: Optional[Dict[str, Any]] = None):
    """Assert that a Manager object is valid and matches expected values."""
    # Basic validation
    assert manager is not None, "Manager should not be None"
    assert manager.id is not None, "Manager should have an ID"
    assert manager.manager_id is not None, "Manager should have a manager_id"
    assert manager.user_id is not None, "Manager should have a user_id"
    assert manager.full_name is not None, "Manager should have a full_name"
    assert manager.department is not None, "Manager should have a department"
    assert manager.created_at is not None, "Manager should have a created_at timestamp"
    
    # Format validations
    assert len(manager.manager_id.strip()) > 0, "Manager ID should not be empty"
    assert len(manager.full_name.strip()) > 0, "Full name should not be empty"
    assert len(manager.department.strip()) > 0, "Department should not be empty"
    
    # Optional fields validation
    if manager.email:
        assert "@" in manager.email, "Manager email should contain @ symbol if provided"
    
    if manager.phone:
        assert len(manager.phone.strip()) > 0, "Phone should not be empty if provided"
    
    # Expected values validation
    if expected_values:
        for key, expected_value in expected_values.items():
            actual_value = getattr(manager, key, None)
            assert actual_value == expected_value, \
                f"Expected {key}={expected_value}, got {actual_value}"


def assert_daily_status_valid(
    daily_status: DailyStatus, 
    expected_values: Optional[Dict[str, Any]] = None
):
    """Assert that a DailyStatus object is valid and matches expected values."""
    # Basic validation
    assert daily_status is not None, "DailyStatus should not be None"
    assert daily_status.id is not None, "DailyStatus should have an ID"
    assert daily_status.vendor_id is not None, "DailyStatus should have a vendor_id"
    assert daily_status.status_date is not None, "DailyStatus should have a status_date"
    assert daily_status.status is not None, "DailyStatus should have a status"
    assert daily_status.submitted_at is not None, "DailyStatus should have a submitted_at timestamp"
    
    # Type validations
    assert isinstance(daily_status.status_date, date), "Status date should be a date object"
    assert isinstance(daily_status.status, AttendanceStatus), \
        "Status should be an AttendanceStatus enum"
    assert isinstance(daily_status.approval_status, ApprovalStatus), \
        "Approval status should be an ApprovalStatus enum"
    
    # Status validation
    assert daily_status.status in [
        AttendanceStatus.IN_OFFICE_FULL, AttendanceStatus.IN_OFFICE_HALF,
        AttendanceStatus.WFH_FULL, AttendanceStatus.WFH_HALF,
        AttendanceStatus.LEAVE_FULL, AttendanceStatus.LEAVE_HALF,
        AttendanceStatus.ABSENT
    ], f"Invalid attendance status: {daily_status.status}"
    
    # Time validations
    if daily_status.in_time:
        assert isinstance(daily_status.in_time, time), "In time should be a time object"
    
    if daily_status.out_time:
        assert isinstance(daily_status.out_time, time), "Out time should be a time object"
    
    if daily_status.in_time and daily_status.out_time:
        # Convert to datetime for comparison
        in_datetime = datetime.combine(daily_status.status_date, daily_status.in_time)
        out_datetime = datetime.combine(daily_status.status_date, daily_status.out_time)
        assert out_datetime > in_datetime, "Out time should be after in time"
    
    # Hours validation
    if daily_status.total_hours:
        assert isinstance(daily_status.total_hours, (int, float)), \
            "Total hours should be numeric"
        assert 0 <= daily_status.total_hours <= 24, \
            f"Total hours should be between 0 and 24, got {daily_status.total_hours}"
    
    # Half-day validation
    if daily_status.is_half_day():
        if daily_status.total_hours:
            assert daily_status.total_hours <= 12, \
                "Half day should not exceed 12 hours"
    
    # Expected values validation
    if expected_values:
        for key, expected_value in expected_values.items():
            actual_value = getattr(daily_status, key, None)
            assert actual_value == expected_value, \
                f"Expected {key}={expected_value}, got {actual_value}"


def assert_api_response_valid(
    response, 
    expected_status: int = 200,
    expected_content_type: str = "text/html",
    required_content: Optional[List[str]] = None,
    forbidden_content: Optional[List[str]] = None
):
    """Assert that an API response is valid."""
    # Status code validation
    assert response.status_code == expected_status, \
        f"Expected status {expected_status}, got {response.status_code}. " \
        f"Response: {response.get_data(as_text=True)[:500]}"
    
    # Content type validation
    if expected_content_type:
        content_type = response.content_type
        if content_type:
            assert expected_content_type in content_type.lower(), \
                f"Expected content type {expected_content_type}, got {content_type}"
    
    # Required content validation
    if required_content:
        response_text = response.get_data(as_text=True)
        for content in required_content:
            assert content in response_text, \
                f"Expected '{content}' in response, but not found. " \
                f"Response: {response_text[:500]}"
    
    # Forbidden content validation
    if forbidden_content:
        response_text = response.get_data(as_text=True)
        for content in forbidden_content:
            assert content not in response_text, \
                f"Found forbidden content '{content}' in response. " \
                f"Response: {response_text[:500]}"


def assert_json_response_valid(
    response,
    expected_status: int = 200,
    required_keys: Optional[List[str]] = None,
    expected_values: Optional[Dict[str, Any]] = None
):
    """Assert that a JSON API response is valid."""
    # Status code validation
    assert response.status_code == expected_status, \
        f"Expected status {expected_status}, got {response.status_code}"
    
    # Content type validation
    content_type = response.content_type
    assert content_type and "application/json" in content_type.lower(), \
        f"Expected JSON content type, got {content_type}"
    
    # Parse JSON
    try:
        json_data = response.get_json()
    except Exception as e:
        assert False, f"Failed to parse JSON response: {e}"
    
    assert json_data is not None, "Response should contain valid JSON data"
    
    # Required keys validation
    if required_keys:
        for key in required_keys:
            assert key in json_data, \
                f"Required key '{key}' not found in JSON response: {json_data}"
    
    # Expected values validation
    if expected_values:
        for key, expected_value in expected_values.items():
            assert key in json_data, f"Key '{key}' not found in JSON response"
            actual_value = json_data[key]
            assert actual_value == expected_value, \
                f"Expected {key}={expected_value}, got {actual_value}"
    
    return json_data


def assert_database_state_valid(expected_counts: Dict[str, int]):
    """Assert that the database contains expected number of records."""
    from models import db, User, Vendor, Manager, DailyStatus
    
    model_mapping = {
        'users': User,
        'vendors': Vendor,
        'managers': Manager,
        'daily_statuses': DailyStatus
    }
    
    for table_name, expected_count in expected_counts.items():
        if table_name in model_mapping:
            model_class = model_mapping[table_name]
            actual_count = db.session.query(model_class).count()
            assert actual_count == expected_count, \
                f"Expected {expected_count} {table_name}, got {actual_count}"


def assert_form_errors(response, expected_errors: List[str]):
    """Assert that form validation errors are present in response."""
    response_text = response.get_data(as_text=True)
    
    for error in expected_errors:
        assert error in response_text, \
            f"Expected form error '{error}' not found in response"


def assert_flash_messages(response, expected_messages: List[str]):
    """Assert that flash messages are present in response."""
    response_text = response.get_data(as_text=True)
    
    for message in expected_messages:
        assert message in response_text, \
            f"Expected flash message '{message}' not found in response"


def assert_user_permissions(user: User, expected_permissions: List[str]):
    """Assert that user has expected permissions based on role."""
    role_permissions = {
        UserRole.VENDOR: ['view_own_data', 'submit_status'],
        UserRole.MANAGER: ['view_own_data', 'submit_status', 'view_team_data', 'approve_status'],
        UserRole.ADMIN: [
            'view_own_data', 'submit_status', 'view_team_data', 'approve_status',
            'manage_users', 'system_config', 'view_all_data'
        ]
    }
    
    user_permissions = role_permissions.get(user.role, [])
    
    for permission in expected_permissions:
        assert permission in user_permissions, \
            f"User with role {user.role} should not have permission '{permission}'"
