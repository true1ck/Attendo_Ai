"""
Pytest Configuration and Global Fixtures
========================================

This file contains pytest configuration and shared fixtures used across all tests.
"""

import os
import sys
import pytest
import tempfile
from datetime import datetime, date, time
from pathlib import Path

# Add the project root to Python path for imports (cross-platform)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Flask and database imports
try:
    from flask import Flask
    from app import app as flask_app
    from models import db, User, UserRole, Vendor, Manager, DailyStatus, AttendanceStatus
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("⚠️ Flask app not available for testing")


@pytest.fixture(scope='session')
def app():
    """Create a Flask app configured for testing."""
    if not FLASK_AVAILABLE:
        pytest.skip("Flask app not available")
    
    # Create a temporary database
    db_fd, db_path = tempfile.mkstemp()
    
    # Use the existing flask_app and configure for testing
    test_app = flask_app
    test_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    test_app.config['TESTING'] = True
    test_app.config['SECRET_KEY'] = 'test-secret-key'
    test_app.config['WTF_CSRF_ENABLED'] = False
    
    # Create application context
    with test_app.app_context():
        db.create_all()
        yield test_app
        
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='function')
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()


@pytest.fixture(scope='function')
def app_context(app):
    """Create an application context."""
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def db_session(app_context):
    """Create a database session for testing."""
    # Clear all tables before each test
    db.drop_all()
    db.create_all()
    
    yield db.session
    
    # Cleanup after test
    db.session.rollback()


@pytest.fixture
def admin_user(db_session):
    """Create a test admin user."""
    user = User(
        username='test_admin',
        email='admin@test.com',
        role=UserRole.ADMIN,
        is_active=True
    )
    user.set_password('admin123')
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def vendor_user(db_session):
    """Create a test vendor user."""
    user = User(
        username='test_vendor',
        email='vendor@test.com',
        role=UserRole.VENDOR,
        is_active=True
    )
    user.set_password('vendor123')
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def manager_user(db_session):
    """Create a test manager user."""
    user = User(
        username='test_manager',
        email='manager@test.com',
        role=UserRole.MANAGER,
        is_active=True
    )
    user.set_password('manager123')
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def test_vendor(db_session, vendor_user, manager_user):
    """Create a test vendor profile."""
    # First create manager profile
    manager = Manager(
        manager_id='MGR001',
        user_id=manager_user.id,
        full_name='Test Manager',
        department='MTB_WCS_MSE7_MS1',
        team_name='Test Team',
        email='manager@test.com',
        phone='+1234567890'
    )
    db_session.add(manager)
    db_session.flush()  # Get the manager ID
    
    # Now create vendor profile
    vendor = Vendor(
        user_id=vendor_user.id,
        vendor_id='VDR001',
        full_name='Test Vendor',
        department='MTB_WCS_MSE7_MS1',
        company='Test Solutions Inc',
        band='B2',
        location='BL-A-5F',
        manager_id=manager.manager_id
    )
    db_session.add(vendor)
    db_session.commit()
    return vendor


@pytest.fixture
def test_manager(db_session, manager_user):
    """Create a test manager profile."""
    manager = Manager(
        manager_id='MGR002',
        user_id=manager_user.id,
        full_name='Test Manager Two',
        department='MTB_WCS_MSE7_MS2',
        team_name='Test Team Two',
        email='manager2@test.com',
        phone='+1234567891'
    )
    db_session.add(manager)
    db_session.commit()
    return manager


@pytest.fixture
def daily_status_today(db_session, test_vendor):
    """Create a daily status for today."""
    status = DailyStatus(
        vendor_id=test_vendor.id,
        status_date=date.today(),
        status=AttendanceStatus.IN_OFFICE_FULL,
        location='Office',
        in_time=time(9, 0),
        out_time=time(18, 0),
        total_hours=8.0,
        comments='Regular work day'
    )
    db_session.add(status)
    db_session.commit()
    return status


@pytest.fixture
def authenticated_vendor_client(client, vendor_user):
    """Create a client with authenticated vendor user."""
    with client.session_transaction() as sess:
        sess['user_id'] = str(vendor_user.id)
        sess['_fresh'] = True
    return client


@pytest.fixture
def authenticated_manager_client(client, manager_user):
    """Create a client with authenticated manager user."""
    with client.session_transaction() as sess:
        sess['user_id'] = str(manager_user.id)
        sess['_fresh'] = True
    return client


@pytest.fixture
def authenticated_admin_client(client, admin_user):
    """Create a client with authenticated admin user."""
    with client.session_transaction() as sess:
        sess['user_id'] = str(admin_user.id)
        sess['_fresh'] = True
    return client


# Pytest configuration
def pytest_configure(config):
    """Pytest configuration hook."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "auth: Authentication tests")
    config.addinivalue_line("markers", "vendor: Vendor functionality tests")
    config.addinivalue_line("markers", "manager: Manager functionality tests")
    config.addinivalue_line("markers", "admin: Admin functionality tests")


# Test collection customization
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add unit marker to all tests by default
        if not any(marker.name in ['integration', 'slow'] for marker in item.iter_markers()):
            item.add_marker(pytest.mark.unit)
            
        # Add specific markers based on file name
        if 'test_auth' in item.nodeid:
            item.add_marker(pytest.mark.auth)
        elif 'test_vendor' in item.nodeid:
            item.add_marker(pytest.mark.vendor)
        elif 'test_manager' in item.nodeid:
            item.add_marker(pytest.mark.manager)
        elif 'test_admin' in item.nodeid:
            item.add_marker(pytest.mark.admin)
