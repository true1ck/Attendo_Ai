"""
Test Helper Functions
====================

Helper functions for creating and managing test objects.
"""

import os
import sys
from typing import Optional, Dict, Any
from datetime import date, time, datetime, timedelta
from pathlib import Path

# Add project root to path (cross-platform)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from models import (
        db, User, UserRole, Vendor, Manager, DailyStatus, 
        AttendanceStatus, ApprovalStatus
    )
    from flask import session
    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False
    print("⚠️ Models not available for test helpers")

from .mock_data import MockDataGenerator


def create_test_user(
    username: Optional[str] = None,
    email: Optional[str] = None,
    password: str = 'testpass123',
    role: UserRole = UserRole.VENDOR,
    is_active: bool = True,
    commit: bool = True
) -> 'User':
    """Create a test user and optionally save to database."""
    if not MODELS_AVAILABLE:
        raise ImportError("Models not available for creating test user")
    
    mock_gen = MockDataGenerator()
    
    if not username:
        username = mock_gen.generate_unique_username()
    if not email:
        email = mock_gen.generate_unique_email(username)
    
    user = User(
        username=username,
        email=email,
        role=role,
        is_active=is_active
    )
    user.set_password(password)
    
    if commit:
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
    
    return user


def create_test_vendor(
    user: Optional['User'] = None,
    vendor_id: Optional[str] = None,
    full_name: Optional[str] = None,
    department: str = 'MTB_WCS_MSE7_MS1',
    company: str = 'Test Solutions Inc',
    band: str = 'B2',
    location: str = 'BL-A-5F',
    manager_id: Optional[str] = None,
    commit: bool = True,
    **kwargs
) -> 'Vendor':
    """Create a test vendor and optionally save to database."""
    if not MODELS_AVAILABLE:
        raise ImportError("Models not available for creating test vendor")
    
    mock_gen = MockDataGenerator()
    
    # Create user if not provided
    if not user:
        user = create_test_user(role=UserRole.VENDOR, commit=commit)
    
    if not vendor_id:
        vendor_id = mock_gen.generate_unique_vendor_id()
    
    if not full_name:
        full_name = f"{user.username.replace('.', ' ').title()}"
    
    vendor = Vendor(
        user_id=user.id,
        vendor_id=vendor_id,
        full_name=full_name,
        department=department,
        company=company,
        band=band,
        location=location,
        manager_id=manager_id,
        **kwargs
    )
    
    if commit:
        db.session.add(vendor)
        db.session.commit()
        db.session.refresh(vendor)
    
    return vendor


def create_test_manager(
    user: Optional['User'] = None,
    manager_id: Optional[str] = None,
    full_name: Optional[str] = None,
    department: str = 'MTB_WCS_MSE7_MS1',
    team_name: str = 'Test Team',
    email: Optional[str] = None,
    phone: Optional[str] = None,
    commit: bool = True,
    **kwargs
) -> 'Manager':
    """Create a test manager and optionally save to database."""
    if not MODELS_AVAILABLE:
        raise ImportError("Models not available for creating test manager")
    
    mock_gen = MockDataGenerator()
    
    # Create user if not provided
    if not user:
        user = create_test_user(role=UserRole.MANAGER, commit=commit)
    
    if not manager_id:
        manager_id = mock_gen.generate_unique_manager_id()
    
    if not full_name:
        full_name = f"{user.username.replace('.', ' ').title()}"
    
    if not email:
        email = user.email
    
    if not phone:
        phone = mock_gen.generate_phone_number()
    
    manager = Manager(
        user_id=user.id,
        manager_id=manager_id,
        full_name=full_name,
        department=department,
        team_name=team_name,
        email=email,
        phone=phone,
        **kwargs
    )
    
    if commit:
        db.session.add(manager)
        db.session.commit()
        db.session.refresh(manager)
    
    return manager


def create_test_daily_status(
    vendor: Optional['Vendor'] = None,
    status_date: Optional[date] = None,
    status: AttendanceStatus = AttendanceStatus.IN_OFFICE_FULL,
    location: str = 'Office',
    in_time: Optional[time] = None,
    out_time: Optional[time] = None,
    total_hours: Optional[float] = None,
    comments: str = 'Test status entry',
    approval_status: ApprovalStatus = ApprovalStatus.PENDING,
    commit: bool = True,
    **kwargs
) -> 'DailyStatus':
    """Create a test daily status and optionally save to database."""
    if not MODELS_AVAILABLE:
        raise ImportError("Models not available for creating test daily status")
    
    # Create vendor if not provided
    if not vendor:
        vendor = create_test_vendor(commit=commit)
    
    if not status_date:
        status_date = date.today()
    
    if not in_time:
        in_time = time(9, 0)
    
    if not out_time:
        out_time = time(17, 0)
    
    if not total_hours:
        # Calculate hours based on times
        start_dt = datetime.combine(status_date, in_time)
        end_dt = datetime.combine(status_date, out_time)
        total_hours = (end_dt - start_dt).total_seconds() / 3600
    
    daily_status = DailyStatus(
        vendor_id=vendor.id,
        status_date=status_date,
        status=status,
        location=location,
        in_time=in_time,
        out_time=out_time,
        total_hours=total_hours,
        comments=comments,
        approval_status=approval_status,
        **kwargs
    )
    
    if commit:
        db.session.add(daily_status)
        db.session.commit()
        db.session.refresh(daily_status)
    
    return daily_status


def login_user(client, user: 'User') -> bool:
    """Log in a user using the test client."""
    try:
        with client.session_transaction() as sess:
            sess['user_id'] = str(user.id)
            sess['_fresh'] = True
            sess['role'] = user.role.value
        return True
    except Exception as e:
        print(f"Failed to login user: {e}")
        return False


def logout_user(client) -> bool:
    """Log out the current user using the test client."""
    try:
        with client.session_transaction() as sess:
            sess.clear()
        return True
    except Exception as e:
        print(f"Failed to logout user: {e}")
        return False


def create_test_team(
    team_size: int = 3,
    manager_name: str = 'Test Manager',
    commit: bool = True
) -> Dict[str, Any]:
    """Create a complete test team with manager and vendors."""
    if not MODELS_AVAILABLE:
        raise ImportError("Models not available for creating test team")
    
    # Create manager
    manager_user = create_test_user(
        username=manager_name.lower().replace(' ', '.'),
        role=UserRole.MANAGER,
        commit=commit
    )
    
    manager = create_test_manager(
        user=manager_user,
        full_name=manager_name,
        commit=commit
    )
    
    # Create vendors
    vendors = []
    for i in range(team_size):
        vendor_name = f"Test Vendor {i+1}"
        vendor_user = create_test_user(
            username=vendor_name.lower().replace(' ', '.'),
            role=UserRole.VENDOR,
            commit=commit
        )
        
        vendor = create_test_vendor(
            user=vendor_user,
            full_name=vendor_name,
            manager_id=manager.manager_id,
            department=manager.department,
            commit=commit
        )
        vendors.append(vendor)
    
    return {
        'manager': manager,
        'manager_user': manager_user,
        'vendors': vendors,
        'vendor_users': [v.user for v in vendors]
    }


def cleanup_test_data():
    """Clean up all test data from database."""
    if not MODELS_AVAILABLE:
        return
    
    try:
        # Delete in reverse dependency order
        db.session.query(DailyStatus).delete()
        db.session.query(Vendor).delete()
        db.session.query(Manager).delete()
        db.session.query(User).delete()
        db.session.commit()
        print("Test data cleaned up successfully")
    except Exception as e:
        db.session.rollback()
        print(f"Failed to clean up test data: {e}")


def create_sample_work_week(
    vendor: 'Vendor',
    start_date: Optional[date] = None,
    include_weekend: bool = False
) -> list:
    """Create a sample work week with daily statuses."""
    if not start_date:
        start_date = date.today() - timedelta(days=7)
    
    statuses = []
    mock_gen = MockDataGenerator()
    
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        
        # Skip weekends unless requested
        if not include_weekend and current_date.weekday() >= 5:
            continue
        
        status_data = mock_gen.create_mock_daily_status(
            vendor.id, 
            current_date
        )
        
        daily_status = create_test_daily_status(
            vendor=vendor,
            **status_data,
            commit=True
        )
        statuses.append(daily_status)
    
    return statuses


def assert_user_can_access_route(client, user: 'User', route: str, method: str = 'GET'):
    """Assert that user can access a specific route."""
    login_user(client, user)
    
    if method.upper() == 'GET':
        response = client.get(route)
    elif method.upper() == 'POST':
        response = client.post(route)
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    assert response.status_code != 401, f"User {user.username} should be able to access {route}"
    assert response.status_code != 403, f"User {user.username} should have permission to access {route}"
    
    return response


def assert_user_cannot_access_route(client, user: 'User', route: str, method: str = 'GET'):
    """Assert that user cannot access a specific route."""
    login_user(client, user)
    
    if method.upper() == 'GET':
        response = client.get(route)
    elif method.upper() == 'POST':
        response = client.post(route)
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    assert response.status_code in [401, 403], \
        f"User {user.username} should not be able to access {route}"
    
    return response
