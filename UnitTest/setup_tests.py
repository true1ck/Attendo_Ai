#!/usr/bin/env python3
"""
Test Environment Setup Script
=============================

This script sets up the testing environment on a new machine after cloning from GitHub.
It handles dependency installation, environment validation, and initial test runs.

Usage:
    python UnitTest/setup_tests.py
    python UnitTest/setup_tests.py --check-only
    python UnitTest/setup_tests.py --install-deps
"""

import sys
import os
import subprocess
import platform
from pathlib import Path


def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print("="*60)


def print_status(message, status="INFO"):
    """Print a status message."""
    icons = {
        "INFO": "ℹ️",
        "SUCCESS": "✅",
        "WARNING": "⚠️",
        "ERROR": "❌"
    }
    print(f"{icons.get(status, 'ℹ️')} {message}")


def run_command(cmd, description="", capture_output=True):
    """Run a command and return success status."""
    print_status(f"Running: {description or ' '.join(cmd)}")
    
    try:
        if capture_output:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode == 0:
                print_status("Command completed successfully", "SUCCESS")
                return True, result.stdout, result.stderr
            else:
                print_status(f"Command failed: {result.stderr}", "ERROR")
                return False, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, check=False)
            success = result.returncode == 0
            status = "SUCCESS" if success else "ERROR"
            print_status(f"Command {'completed' if success else 'failed'}", status)
            return success, "", ""
    except Exception as e:
        print_status(f"Command execution error: {e}", "ERROR")
        return False, "", str(e)


def check_python_version():
    """Check if Python version is compatible."""
    print_header("Python Version Check")
    
    version = sys.version_info
    print_status(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version >= (3, 7):
        print_status("Python version is compatible ✓", "SUCCESS")
        return True
    else:
        print_status("Python 3.7+ is required for this project", "ERROR")
        return False


def check_project_structure():
    """Check if project structure is correct."""
    print_header("Project Structure Check")
    
    # Get current script location
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    
    print_status(f"UnitTest directory: {current_dir}")
    print_status(f"Project root: {project_root}")
    
    # Check essential files
    essential_files = [
        'app.py',
        'models.py', 
        'utils.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file_name in essential_files:
        file_path = project_root / file_name
        if file_path.exists():
            print_status(f"Found {file_name} ✓", "SUCCESS")
        else:
            print_status(f"Missing {file_name} ✗", "ERROR")
            missing_files.append(file_name)
    
    # Check UnitTest structure
    unittest_files = [
        'conftest.py',
        'pytest.ini',
        'requirements-test.txt',
        'run_tests.py'
    ]
    
    for file_name in unittest_files:
        file_path = current_dir / file_name
        if file_path.exists():
            print_status(f"Found UnitTest/{file_name} ✓", "SUCCESS")
        else:
            print_status(f"Missing UnitTest/{file_name} ✗", "ERROR")
            missing_files.append(f"UnitTest/{file_name}")
    
    if not missing_files:
        print_status("All essential files found", "SUCCESS")
        return True
    else:
        print_status(f"Missing files: {', '.join(missing_files)}", "ERROR")
        return False


def check_installed_packages():
    """Check which required packages are installed."""
    print_header("Package Installation Check")
    
    essential_packages = [
        'pytest',
        'flask',
        'sqlalchemy',
    ]
    
    optional_packages = [
        'pytest-cov',
        'pytest-mock',
        'faker',
        'factory-boy'
    ]
    
    installed = []
    missing_essential = []
    missing_optional = []
    
    for package in essential_packages:
        success, _, _ = run_command([sys.executable, '-c', f'import {package}'], 
                                   f"Checking {package}")
        if success:
            installed.append(package)
        else:
            missing_essential.append(package)
    
    for package in optional_packages:
        # Handle special package name mappings
        import_name = package.replace("-", "_")
        if package == 'factory-boy':
            import_name = 'factory'
        
        success, _, _ = run_command([sys.executable, '-c', f'import {import_name}'], 
                                   f"Checking {package}")
        if success:
            installed.append(package)
        else:
            missing_optional.append(package)
    
    print_status(f"Installed packages: {', '.join(installed)}", "SUCCESS")
    
    if missing_essential:
        print_status(f"Missing essential packages: {', '.join(missing_essential)}", "ERROR")
        return False, missing_essential, missing_optional
    
    if missing_optional:
        print_status(f"Missing optional packages: {', '.join(missing_optional)}", "WARNING")
    
    return True, [], missing_optional


def install_dependencies():
    """Install test dependencies."""
    print_header("Installing Dependencies")
    
    current_dir = Path(__file__).parent
    requirements_file = current_dir / 'requirements-test.txt'
    
    if not requirements_file.exists():
        print_status("requirements-test.txt not found", "ERROR")
        return False
    
    print_status(f"Installing from {requirements_file}")
    success, stdout, stderr = run_command([
        sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
    ], "Installing test dependencies", capture_output=True)
    
    if success:
        print_status("Dependencies installed successfully", "SUCCESS")
    else:
        print_status("Failed to install some dependencies", "WARNING")
        print("STDOUT:", stdout)
        print("STDERR:", stderr)
    
    return success


def test_imports():
    """Test that key imports work."""
    print_header("Import Test")
    
    # Add project root to path
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    sys.path.insert(0, str(project_root))
    
    imports_to_test = [
        ('app', 'from app import app'),
        ('models', 'from models import User, UserRole'),
        ('utils', 'from utils import is_weekend'),
        ('UnitTest.utils.mock_data', 'from UnitTest.utils.mock_data import MockDataGenerator'),
        ('UnitTest.utils.test_helpers', 'from UnitTest.utils.test_helpers import create_test_user'),
    ]
    
    failed_imports = []
    
    for name, import_statement in imports_to_test:
        try:
            exec(import_statement)
            print_status(f"Import {name} ✓", "SUCCESS")
        except Exception as e:
            print_status(f"Import {name} ✗ - {e}", "ERROR")
            failed_imports.append(name)
    
    if not failed_imports:
        print_status("All imports successful", "SUCCESS")
        return True
    else:
        print_status(f"Failed imports: {', '.join(failed_imports)}", "ERROR")
        return False


def run_basic_tests():
    """Run basic tests to verify setup."""
    print_header("Running Basic Tests")
    
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    
    # Run the basic test file
    success, stdout, stderr = run_command([
        sys.executable, '-m', 'pytest', 
        str(current_dir / 'tests' / 'test_basic.py'),
        '-v'
    ], "Running basic tests", capture_output=False)
    
    return success


def main():
    """Main setup function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Set up test environment")
    parser.add_argument('--check-only', action='store_true', 
                       help='Only check environment, do not install anything')
    parser.add_argument('--install-deps', action='store_true',
                       help='Install dependencies even if check fails')
    args = parser.parse_args()
    
    print_header("Test Environment Setup")
    print_status(f"Platform: {platform.system()} {platform.release()}")
    print_status(f"Python executable: {sys.executable}")
    
    # Step 1: Check Python version
    if not check_python_version():
        print_status("Setup failed: Incompatible Python version", "ERROR")
        return 1
    
    # Step 2: Check project structure
    if not check_project_structure():
        print_status("Setup failed: Missing project files", "ERROR")
        return 1
    
    # Step 3: Check packages
    packages_ok, missing_essential, missing_optional = check_installed_packages()
    
    # Step 4: Install dependencies if needed and allowed
    if not packages_ok or args.install_deps:
        if args.check_only:
            print_status("Skipping dependency installation (--check-only)", "WARNING")
        else:
            print_status("Installing missing dependencies...")
            if not install_dependencies():
                print_status("Failed to install all dependencies", "WARNING")
            
            # Re-check packages
            packages_ok, missing_essential, missing_optional = check_installed_packages()
    
    # Step 5: Test imports
    if not test_imports():
        print_status("Setup incomplete: Import failures", "ERROR")
        return 1
    
    # Step 6: Run basic tests if everything is okay
    if packages_ok and not args.check_only:
        print_status("Running validation tests...")
        if run_basic_tests():
            print_status("Basic tests passed ✓", "SUCCESS")
        else:
            print_status("Some basic tests failed", "WARNING")
    
    # Final status
    print_header("Setup Complete")
    
    if packages_ok:
        print_status("✅ Test environment is ready!", "SUCCESS")
        print_status("You can now run tests with:")
        print("   python UnitTest/run_tests.py")
        print("   python UnitTest/run_tests.py --verbose")
        print("   python UnitTest/run_tests.py --coverage --html")
        return 0
    else:
        print_status("⚠️ Setup completed with warnings", "WARNING")
        print_status(f"Missing essential packages: {', '.join(missing_essential)}")
        if missing_optional:
            print_status(f"Missing optional packages: {', '.join(missing_optional)}")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
