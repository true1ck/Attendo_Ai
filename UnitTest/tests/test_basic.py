"""
Basic Test
==========

Simple test to verify the testing infrastructure is working.
"""

import pytest
import sys
import os
from datetime import date, datetime
from pathlib import Path

# Add project root to path (cross-platform)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Test basic functionality
class TestBasicInfrastructure:
    """Test basic infrastructure components."""
    
    def test_python_environment(self):
        """Test that Python environment is working."""
        assert sys.version_info >= (3, 7), "Python 3.7+ is required"
        
    def test_imports_work(self):
        """Test that basic imports work."""
        import datetime
        import os
        import sys
        assert datetime is not None
        assert os is not None
        assert sys is not None
        
    def test_project_structure(self):
        """Test that project structure is accessible."""
        # Test that project root exists
        assert project_root.exists(), f"Project root should exist: {project_root}"
        
        # Test that main app files exist
        app_file = project_root / 'app.py'
        models_file = project_root / 'models.py'
        utils_file = project_root / 'utils.py'
        
        assert app_file.exists(), f"app.py should exist: {app_file}"
        assert models_file.exists(), f"models.py should exist: {models_file}"
        assert utils_file.exists(), f"utils.py should exist: {utils_file}"


class TestImportCapabilities:
    """Test that we can import from the main project."""
    
    def test_import_app(self):
        """Test importing the main Flask app."""
        try:
            from app import app
            assert app is not None
            assert hasattr(app, 'config')
        except ImportError as e:
            pytest.fail(f"Failed to import Flask app: {e}")
    
    def test_import_models(self):
        """Test importing models."""
        try:
            from models import User, UserRole, Vendor, Manager, DailyStatus
            assert User is not None
            assert UserRole is not None
            assert Vendor is not None
            assert Manager is not None
            assert DailyStatus is not None
        except ImportError as e:
            pytest.fail(f"Failed to import models: {e}")
    
    def test_import_utils(self):
        """Test importing utility functions."""
        try:
            from utils import is_weekend
            assert is_weekend is not None
            assert callable(is_weekend)
        except ImportError as e:
            pytest.fail(f"Failed to import utils: {e}")


class TestWeekendBasicFunctionality:
    """Test basic weekend functionality without database."""
    
    def test_weekend_function_exists(self):
        """Test that weekend detection function exists."""
        try:
            from utils import is_weekend
            assert callable(is_weekend)
        except ImportError:
            pytest.skip("Weekend function not available")
    
    def test_weekend_detection_saturday(self):
        """Test that Saturday is detected as weekend."""
        try:
            from utils import is_weekend
            # Create a known Saturday (2023-01-07 was a Saturday)
            saturday = date(2023, 1, 7)
            assert is_weekend(saturday) == True, "Saturday should be detected as weekend"
        except ImportError:
            pytest.skip("Weekend function not available")
    
    def test_weekend_detection_sunday(self):
        """Test that Sunday is detected as weekend."""
        try:
            from utils import is_weekend
            # Create a known Sunday (2023-01-08 was a Sunday)
            sunday = date(2023, 1, 8)
            assert is_weekend(sunday) == True, "Sunday should be detected as weekend"
        except ImportError:
            pytest.skip("Weekend function not available")
    
    def test_weekend_detection_monday(self):
        """Test that Monday is not detected as weekend."""
        try:
            from utils import is_weekend
            # Create a known Monday (2023-01-09 was a Monday)
            monday = date(2023, 1, 9)
            assert is_weekend(monday) == False, "Monday should not be detected as weekend"
        except ImportError:
            pytest.skip("Weekend function not available")


class TestTestUtilities:
    """Test that our test utilities work."""
    
    def test_mock_data_generator(self):
        """Test that MockDataGenerator works."""
        from UnitTest.utils.mock_data import MockDataGenerator
        
        generator = MockDataGenerator()
        assert generator is not None
        
        # Test username generation
        username = generator.generate_unique_username()
        assert username is not None
        assert len(username) > 0
        
        # Test email generation  
        email = generator.generate_unique_email()
        assert email is not None
        assert '@' in email
    
    def test_test_helpers_import(self):
        """Test that test helpers can be imported."""
        from UnitTest.utils.test_helpers import create_test_user
        assert callable(create_test_user)


# Mark all tests as unit tests
pytestmark = pytest.mark.unit
