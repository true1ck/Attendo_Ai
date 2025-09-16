# Vendor Timesheet Tool - Unit Tests

This directory contains comprehensive unit and integration tests for the Vendor Timesheet and Attendance Tool.

## 📁 Directory Structure

```
UnitTest/
├── README.md                 # This file
├── __init__.py              # Package initialization
├── conftest.py              # Pytest configuration and fixtures
├── test_config.py           # Test-specific configuration
├── run_tests.py             # Main test runner script
├── run_weekend_holiday_tests.py      # Weekend/holiday test runner ✅
├── test_weekend_holiday_exclusion_standalone.py # Standalone test suite ✅
├── requirements-test.txt    # Test dependencies
│
├── tests/                   # Main test modules
│   ├── __init__.py
│   ├── test_models.py       # Database model tests ✅
│   ├── test_utils_weekend_holiday.py    # Weekend/holiday utils tests ✅
│   ├── test_weekend_holiday_exclusion.py # Weekend/holiday integration tests ✅
│   ├── test_auth.py         # Authentication tests (TODO)
│   ├── test_vendor.py       # Vendor functionality tests (TODO)
│   ├── test_manager.py      # Manager functionality tests (TODO)
│   ├── test_admin.py        # Admin functionality tests (TODO)
│   └── test_integration.py  # Integration tests (TODO)
│
├── utils/                   # Test utilities and helpers
│   ├── __init__.py          # Utils package init
│   ├── test_helpers.py      # Helper functions for testing
│   ├── mock_data.py         # Mock data generator
│   └── assertions.py        # Custom assertion functions
│
└── fixtures/                # Test data and fixtures
    └── (test data files)
```

## 🧪 Test Categories

### ✅ Completed Tests

#### **Model Tests** (`test_models.py`)
- **User Model Tests**
  - User creation and validation
  - Password hashing and verification
  - User roles (Vendor, Manager, Admin)
  - String representation
  
- **Vendor Model Tests**
  - Vendor profile creation
  - Manager-vendor relationships
  - Model relationships and collections
  
- **Manager Model Tests**
  - Manager profile creation
  - Team management functionality
  - Manager-vendor relationships
  
- **DailyStatus Model Tests**
  - Daily status creation and validation
  - Half-day vs full-day functionality
  - Attendance status enums
  - Time validation
  
- **Holiday Model Tests**
  - Holiday creation
  - Date uniqueness constraints
  
- **MismatchRecord Model Tests**
  - Mismatch record creation
  - JSON details storage and retrieval
  - Mismatch summary generation
  
- **Model Relationships Tests**
  - User-Vendor relationships
  - User-Manager relationships
  - Cascade delete behavior
  
- **Model Validation Tests**
  - Unique constraint testing
  - Email and ID uniqueness
  
- **Mock Data Generator Tests**
  - Unique identifier generation
  - Mock data creation for all models
  - Team data generation

#### **Weekend/Holiday Exclusion Tests** (`test_utils_weekend_holiday.py`, `test_weekend_holiday_exclusion.py`) ✅
- **Utility Function Tests**
  - Weekend detection (Saturday/Sunday)
  - Holiday detection from database
  - Non-working day combined checking
  - Reason string generation
  
- **Status Submission Blocking Tests**
  - Prevents submissions on weekends
  - Prevents submissions on holidays
  - UI adaptation and messaging
  - Form validation and error handling
  
- **System Integration Tests**
  - Notification exclusion on non-working days
  - Mismatch detection skips weekends/holidays
  - Working day calculations exclude non-working days
  - Late submission checks return empty appropriately
  
- **Working Day Calculation Tests**
  - Accurate business day counting
  - Weekend exclusion validation
  - Holiday exclusion validation
  - Date range processing

- **Standalone Test Suite**
  - Context-free utility testing
  - Mock-based integration testing
  - Quick validation without Flask app

### 🔄 TODO: Remaining Tests

#### **Authentication Tests** (`test_auth.py`)
- [ ] Login/logout functionality
- [ ] Password validation
- [ ] Session management
- [ ] Role-based access control
- [ ] User registration
- [ ] Password reset

#### **Vendor Functionality Tests** (`test_vendor.py`)
- [ ] Vendor dashboard access
- [ ] Daily status submission
- [ ] Status history viewing
- [ ] Mismatch resolution
- [ ] Profile management

#### **Manager Functionality Tests** (`test_manager.py`)
- [ ] Manager dashboard
- [ ] Team status overview
- [ ] Approval workflows
- [ ] Team management
- [ ] Notification preferences

#### **Admin Functionality Tests** (`test_admin.py`)
- [ ] System configuration
- [ ] User management (CRUD)
- [ ] Holiday management
- [ ] Reports generation
- [ ] System monitoring

#### **Integration Tests** (`test_integration.py`)
- [ ] API endpoints testing
- [ ] Database operations
- [ ] Workflow integrations
- [ ] Data import/export
- [ ] Notification systems

## 🚀 Quick Start

### Prerequisites

```bash
# Install Python dependencies
pip install pytest pytest-cov pytest-mock flask-testing

# Or install from requirements file (when created)
pip install -r UnitTest/requirements-test.txt
```

### Running Tests

#### Using the Test Runner (Recommended)

```bash
# Run all tests
python UnitTest/run_tests.py

# Run specific test categories
python UnitTest/run_tests.py --models        # Only model tests
python UnitTest/run_tests.py --weekend       # Only weekend/holiday exclusion tests
python UnitTest/run_tests.py --standalone    # Only standalone weekend/holiday tests
python UnitTest/run_tests.py --auth          # Only auth tests
python UnitTest/run_tests.py --vendor        # Only vendor tests
python UnitTest/run_tests.py --manager       # Only manager tests
python UnitTest/run_tests.py --admin         # Only admin tests
python UnitTest/run_tests.py --integration   # Only integration tests

# Run with coverage report
python UnitTest/run_tests.py --coverage --html

# Run with verbose output
python UnitTest/run_tests.py --verbose

# Skip slow tests
python UnitTest/run_tests.py --fast
```

#### Using Pytest Directly

```bash
# Run all tests
pytest UnitTest/

# Run specific test file
pytest UnitTest/tests/test_models.py

# Run with coverage
pytest UnitTest/ --cov=backend --cov=models --cov-report=html

# Run specific test class
pytest UnitTest/tests/test_models.py::TestUser

# Run specific test method
pytest UnitTest/tests/test_models.py::TestUser::test_create_user

# Run tests with markers
pytest UnitTest/ -m unit              # Only unit tests
pytest UnitTest/ -m "not slow"        # Skip slow tests
pytest UnitTest/ -m auth               # Only auth tests
```

## 📊 Test Coverage

Current test coverage focuses on database models. To check coverage:

```bash
# Generate coverage report
python UnitTest/run_tests.py --coverage --html

# View HTML report
open htmlcov/index.html
```

**Coverage Goals:**
- Overall: > 80%
- Models: > 90% ✅
- Views/Routes: > 80% (TODO)
- Business Logic: > 85% (TODO)

## 🏗️ Test Infrastructure

### Fixtures (`conftest.py`)

Pre-configured test fixtures available in all tests:

- `app`: Flask application instance
- `client`: Test client for HTTP requests
- `db_session`: Database session for each test
- `admin_user`: Test admin user
- `vendor_user`: Test vendor user  
- `manager_user`: Test manager user
- `test_vendor`: Complete vendor profile
- `test_manager`: Complete manager profile
- `daily_status_today`: Sample daily status

### Test Utilities (`utils/`)

- **test_helpers.py**: Helper functions for creating test data
- **mock_data.py**: Realistic mock data generation
- **assertions.py**: Custom assertion functions for validation

### Configuration (`test_config.py`)

Test-specific configuration including:
- Test database settings
- Mock API endpoints
- Test user credentials
- Performance thresholds

## 📝 Writing Tests

### Test Structure

```python
import pytest
from UnitTest.utils import create_test_user, assert_user_valid

@pytest.mark.unit
class TestMyFeature:
    """Test cases for My Feature."""
    
    def test_basic_functionality(self, db_session):
        """Test basic functionality."""
        # Arrange
        user = create_test_user(username='testuser')
        
        # Act
        result = some_function(user)
        
        # Assert
        assert result is not None
        assert_user_valid(user)
```

### Test Markers

Available pytest markers:
- `@pytest.mark.unit`: Unit tests (default)
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.slow`: Slow-running tests
- `@pytest.mark.auth`: Authentication tests
- `@pytest.mark.vendor`: Vendor functionality
- `@pytest.mark.manager`: Manager functionality
- `@pytest.mark.admin`: Admin functionality

### Custom Assertions

Use custom assertion functions for better error messages:

```python
from UnitTest.utils.assertions import assert_user_valid, assert_api_response_valid

def test_user_creation(self, db_session):
    user = create_user(...)
    assert_user_valid(user, expected_values={'username': 'testuser'})

def test_api_endpoint(self, client):
    response = client.get('/api/vendors')
    assert_api_response_valid(
        response, 
        expected_status=200,
        required_content=['vendor_id', 'full_name']
    )
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure you're running from project root
   cd /path/to/attendo-SubReady
   python UnitTest/run_tests.py
   ```

2. **Database Errors**
   ```bash
   # Clean test artifacts
   python UnitTest/run_tests.py --clean
   ```

3. **Missing Dependencies**
   ```bash
   # Install test dependencies
   python UnitTest/run_tests.py --install-deps
   ```

### Debug Mode

Run tests with verbose output and no capture for debugging:

```bash
python UnitTest/run_tests.py --verbose -x
# or
pytest UnitTest/ -v -s -x
```

## 📈 Test Metrics

Current statistics:
- ✅ **Model Tests**: 100% complete (762 lines, 25+ test cases)
- 🔄 **Auth Tests**: 0% complete (TODO)
- 🔄 **Vendor Tests**: 0% complete (TODO)
- 🔄 **Manager Tests**: 0% complete (TODO)
- 🔄 **Admin Tests**: 0% complete (TODO)
- 🔄 **Integration Tests**: 0% complete (TODO)

## 🎯 Next Steps

1. **Create Authentication Tests** - Login/logout, role validation
2. **Create Vendor Functionality Tests** - Dashboard, status submission  
3. **Create Manager Tests** - Team management, approvals
4. **Create Admin Tests** - System configuration, user management
5. **Create Integration Tests** - End-to-end workflows
6. **Add Performance Tests** - Response time, load testing
7. **Create Test Data Fixtures** - Sample data files
8. **Add API Documentation Tests** - Swagger/OpenAPI validation

## 📞 Support

For questions about the test suite:
1. Check this README
2. Review existing test examples in `test_models.py`
3. Check the test utilities in `utils/`
4. Review pytest documentation

---

**Happy Testing! 🧪✨**
