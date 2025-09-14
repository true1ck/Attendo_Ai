"""
Tests Package
=============

This package contains all test modules for the Vendor Timesheet Tool.

Test Organization:
- test_models.py: Database model tests
- test_auth.py: Authentication and authorization tests  
- test_vendor.py: Vendor functionality tests
- test_manager.py: Manager functionality tests
- test_admin.py: Admin functionality tests
- test_integration.py: Integration and workflow tests
"""

# Test configuration
import pytest

# Configure pytest markers
pytestmark = pytest.mark.unit
