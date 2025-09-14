"""
Vendor Timesheet Tool - Unit Test Package
==========================================

This package contains comprehensive unit and integration tests for the 
Vendor Timesheet and Attendance Tool.

Test Structure:
- tests/: Main test modules organized by functionality
- fixtures/: Test data and mock objects
- utils/: Test utilities and helper functions

Usage:
- Run all tests: python -m pytest UnitTest/
- Run specific test: python -m pytest UnitTest/tests/test_models.py
- Run with coverage: python -m pytest UnitTest/ --cov=backend --cov-report=html
"""

__version__ = "1.0.0"
__author__ = "Vendor Timesheet Tool Team"

# Make key test utilities available at package level
from .utils.test_helpers import create_test_user, create_test_vendor, create_test_manager
from .utils.mock_data import MockDataGenerator

__all__ = [
    'create_test_user',
    'create_test_vendor', 
    'create_test_manager',
    'MockDataGenerator'
]
