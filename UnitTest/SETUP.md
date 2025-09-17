# UnitTest Setup Guide

## 🚀 Quick Setup for New Environments

This guide helps you set up the testing environment after cloning the project on a new machine.

### Prerequisites

- **Python 3.7+** (Required)
- **Git** (for cloning)
- **Internet connection** (for installing dependencies)

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd <project-directory>
```

### Step 2: Run the Setup Script (Recommended)

The setup script will automatically check your environment and install dependencies:

```bash
# Automatic setup with dependency installation
python UnitTest/setup_tests.py

# Or check environment without installing anything
python UnitTest/setup_tests.py --check-only

# Or force install dependencies
python UnitTest/setup_tests.py --install-deps
```

### Step 3: Manual Setup (Alternative)

If you prefer manual setup:

#### 3.1 Install Test Dependencies

```bash
# Install test dependencies
pip install -r UnitTest/requirements-test.txt

# If some packages fail, install the essential ones:
pip install pytest pytest-cov pytest-mock flask-testing factory-boy faker
```

#### 3.2 Install Main Project Dependencies

```bash
# Install main project dependencies
pip install -r requirements.txt
```

### Step 4: Verify Setup

Run the basic tests to ensure everything works:

```bash
# From project root directory
python UnitTest/run_tests.py --verbose
```

Expected output:
```
🧪 Vendor Timesheet Tool - Test Runner
==================================================
...
✅ All tests passed!
```

## 🔧 Platform-Specific Notes

### Windows
- Use **PowerShell** or **Command Prompt**
- Paths use backslashes but are handled automatically
- Ensure Python is in your PATH

### macOS/Linux
- Use **Terminal**  
- Paths use forward slashes but are handled automatically
- You may need to use `python3` instead of `python`

### Python Virtual Environments (Recommended)

Create a virtual environment to isolate dependencies:

```bash
# Create virtual environment
python -m venv test-env

# Activate it
# Windows:
test-env\Scripts\activate
# macOS/Linux:
source test-env/bin/activate

# Now install dependencies
python UnitTest/setup_tests.py
```

## 📁 Directory Structure

After setup, your project should look like:

```
project-root/
├── app.py                     # Main Flask app
├── models.py                  # Database models
├── utils.py                   # Utility functions
├── requirements.txt           # Main dependencies
├── UnitTest/                  # Test directory
│   ├── setup_tests.py         # Setup script
│   ├── run_tests.py           # Test runner
│   ├── requirements-test.txt  # Test dependencies
│   ├── pytest.ini            # Pytest config
│   ├── conftest.py            # Test fixtures
│   ├── tests/                 # Test files
│   │   └── test_basic.py      # Basic tests
│   └── utils/                 # Test utilities
│       ├── test_helpers.py    # Helper functions
│       ├── mock_data.py       # Mock data generator
│       └── assertions.py      # Custom assertions
```

## 🧪 Running Tests

### Basic Commands

```bash
# Run all tests
python UnitTest/run_tests.py

# Run with verbose output
python UnitTest/run_tests.py --verbose

# Run with coverage report
python UnitTest/run_tests.py --coverage --html

# Run specific test categories (when available)
python UnitTest/run_tests.py --models
python UnitTest/run_tests.py --auth
python UnitTest/run_tests.py --weekend
```

### Using pytest directly

```bash
# From project root
python -m pytest UnitTest/ -v

# Run specific test file
python -m pytest UnitTest/tests/test_basic.py -v

# Run with coverage
python -m pytest UnitTest/ --cov=models --cov=utils --cov-report=html
```

## 🔍 Troubleshooting

### Common Issues

#### Import Errors
```
ModuleNotFoundError: No module named 'app'
```
**Solution:** Make sure you're running tests from the project root directory.

#### Missing Dependencies
```
ModuleNotFoundError: No module named 'pytest'
```
**Solution:** Install test dependencies:
```bash
pip install -r UnitTest/requirements-test.txt
```

#### Path Issues
```
FileNotFoundError: requirements-test.txt
```
**Solution:** Run commands from the project root directory, not the UnitTest directory.

#### Flask App Issues
```
ImportError while loading conftest
```
**Solution:** Ensure the main Flask app and models can be imported:
```bash
python -c "from app import app; print('OK')"
python -c "from models import User; print('OK')"
```

### Environment Check

Run the setup script in check-only mode to diagnose issues:

```bash
python UnitTest/setup_tests.py --check-only
```

This will show:
- ✅ Python version compatibility
- ✅ Project structure validation  
- ✅ Package installation status
- ✅ Import capabilities
- ❌ Any issues found

## 📊 Expected Test Results

After successful setup, you should see:

```
Platform: Windows/macOS/Linux
Python version: 3.x.x ✓
All essential files found ✓
All imports successful ✓
12 passed in 0.xx seconds ✅
Test environment is ready! ✅
```

## 🚀 Next Steps

Once setup is complete:

1. **Add More Tests**: Create test files in `UnitTest/tests/`
2. **Run Regular Tests**: Use `python UnitTest/run_tests.py`
3. **View Coverage**: Run with `--coverage --html` and open `htmlcov/index.html`
4. **Debug Issues**: Use `--verbose` for detailed output

## 🆘 Support

If you encounter issues:

1. Check this SETUP.md guide
2. Run `python UnitTest/setup_tests.py --check-only`
3. Ensure you're in the correct directory
4. Verify Python 3.7+ is installed
5. Check that the project structure matches the expected layout

---

**Happy Testing! 🧪✨**
