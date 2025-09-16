#!/usr/bin/env python3
"""
Test Runner Script
==================

This script provides an easy way to run all tests or specific test suites
for the Vendor Timesheet Tool.

Usage:
    python UnitTest/run_tests.py                    # Run all tests
    python UnitTest/run_tests.py --models           # Run only model tests
    python UnitTest/run_tests.py --auth             # Run only auth tests
    python UnitTest/run_tests.py --vendor           # Run only vendor tests
    python UnitTest/run_tests.py --manager          # Run only manager tests
    python UnitTest/run_tests.py --admin            # Run only admin tests
    python UnitTest/run_tests.py --integration      # Run only integration tests
    python UnitTest/run_tests.py --weekend          # Run weekend/holiday exclusion tests
    python UnitTest/run_tests.py --standalone       # Run standalone weekend/holiday tests
    python UnitTest/run_tests.py --coverage         # Run with coverage report
    python UnitTest/run_tests.py --verbose          # Run with verbose output
    python UnitTest/run_tests.py --fast             # Skip slow tests
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_command(cmd, description=""):
    """Run a shell command and return the result."""
    print(f"\n{'='*50}")
    print(f"🔄 {description}")
    print(f"{'='*50}")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True, cwd=project_root)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(
        description="Test runner for Vendor Timesheet Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python UnitTest/run_tests.py --models --verbose
  python UnitTest/run_tests.py --coverage --html
  python UnitTest/run_tests.py --fast --unit
        """
    )
    
    # Test selection arguments
    parser.add_argument('--models', action='store_true', help='Run model tests only')
    parser.add_argument('--auth', action='store_true', help='Run authentication tests only')
    parser.add_argument('--vendor', action='store_true', help='Run vendor functionality tests only')
    parser.add_argument('--manager', action='store_true', help='Run manager functionality tests only')
    parser.add_argument('--admin', action='store_true', help='Run admin functionality tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests only')
    parser.add_argument('--weekend', action='store_true', help='Run weekend/holiday exclusion tests only')
    parser.add_argument('--standalone', action='store_true', help='Run standalone weekend/holiday tests')
    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--slow', action='store_true', help='Include slow tests')
    parser.add_argument('--fast', action='store_true', help='Skip slow tests')
    
    # Output and reporting arguments
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet output')
    parser.add_argument('--coverage', action='store_true', help='Run with coverage report')
    parser.add_argument('--html', action='store_true', help='Generate HTML coverage report')
    parser.add_argument('--xml', action='store_true', help='Generate XML coverage report')
    
    # Test execution arguments
    parser.add_argument('--parallel', '-n', type=int, help='Run tests in parallel (specify number of workers)')
    parser.add_argument('--failed-first', action='store_true', help='Run failed tests first')
    parser.add_argument('--exitfirst', '-x', action='store_true', help='Exit on first failure')
    parser.add_argument('--tb', choices=['short', 'long', 'line', 'no'], default='short', help='Traceback style')
    
    # Additional arguments
    parser.add_argument('--install-deps', action='store_true', help='Install test dependencies first')
    parser.add_argument('--clean', action='store_true', help='Clean test artifacts before running')
    parser.add_argument('test_files', nargs='*', help='Specific test files to run')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.fast and args.slow:
        print("❌ Cannot specify both --fast and --slow")
        return 1
    
    if args.verbose and args.quiet:
        print("❌ Cannot specify both --verbose and --quiet")
        return 1
    
    # Print header
    print("🧪 Vendor Timesheet Tool - Test Runner")
    print("=" * 50)
    
    # Install dependencies if requested
    if args.install_deps:
        print("\n📦 Installing test dependencies...")
        deps_cmd = [sys.executable, '-m', 'pip', 'install', '-r', 'requirements-test.txt']
        if not run_command(deps_cmd, "Installing test dependencies"):
            print("❌ Failed to install dependencies")
            return 1
    
    # Clean test artifacts if requested
    if args.clean:
        print("\n🧹 Cleaning test artifacts...")
        clean_paths = [
            '.pytest_cache',
            'htmlcov',
            '.coverage',
            'coverage.xml',
            'test-results.xml'
        ]
        
        for path in clean_paths:
            full_path = project_root / path
            if full_path.exists():
                if full_path.is_dir():
                    import shutil
                    shutil.rmtree(full_path)
                else:
                    full_path.unlink()
                print(f"   Removed: {path}")
    
    # Build pytest command
    cmd = [sys.executable, '-m', 'pytest']
    
    # Test discovery path
    test_path = 'UnitTest/'
    
    # Specific test selection
    specific_tests = []
    if args.models:
        specific_tests.append('UnitTest/tests/test_models.py')
    if args.auth:
        specific_tests.append('UnitTest/tests/test_auth.py')
    if args.vendor:
        specific_tests.append('UnitTest/tests/test_vendor.py')
    if args.manager:
        specific_tests.append('UnitTest/tests/test_manager.py')
    if args.admin:
        specific_tests.append('UnitTest/tests/test_admin.py')
    if args.integration:
        specific_tests.append('UnitTest/tests/test_integration.py')
    if args.weekend:
        specific_tests.extend([
            'UnitTest/tests/test_utils_weekend_holiday.py',
            'UnitTest/tests/test_weekend_holiday_simple.py'
        ])
    
    # Handle standalone weekend/holiday tests
    if args.standalone:
        print("\n🔄 Running standalone weekend/holiday tests...")
        try:
            from run_weekend_holiday_tests import main as run_standalone
            return run_standalone()
        except ImportError:
            print("❌ Standalone test runner not found")
            return 1
    
    if args.test_files:
        specific_tests.extend(args.test_files)
    
    if specific_tests:
        cmd.extend(specific_tests)
    else:
        cmd.append(test_path)
    
    # Test markers
    markers = []
    if args.unit:
        markers.append('unit')
    if args.fast:
        markers.append('not slow')
    if args.slow:
        markers.append('slow')
    
    if markers:
        cmd.extend(['-m', ' and '.join(markers)])
    
    # Output control
    if args.verbose:
        cmd.append('-v')
        cmd.append('-s')  # Don't capture stdout
    elif args.quiet:
        cmd.append('-q')
    
    # Traceback style
    cmd.extend(['--tb', args.tb])
    
    # Test execution options
    if args.exitfirst:
        cmd.append('-x')
    
    if args.failed_first:
        cmd.append('--lf')
    
    if args.parallel:
        cmd.extend(['-n', str(args.parallel)])
    
    # Coverage options
    if args.coverage:
        cmd.extend(['--cov=backend', '--cov=models'])
        cmd.append('--cov-report=term-missing')
        
        if args.html:
            cmd.append('--cov-report=html')
        
        if args.xml:
            cmd.append('--cov-report=xml')
    
    # Additional pytest options
    cmd.extend([
        '--strict-markers',
        '--disable-warnings',
        '--color=yes'
    ])
    
    # Run tests
    success = run_command(cmd, "Running tests")
    
    if success:
        print("\n✅ All tests passed!")
        
        # Show coverage report location if generated
        if args.coverage and args.html:
            coverage_path = project_root / 'htmlcov' / 'index.html'
            if coverage_path.exists():
                print(f"\n📊 HTML coverage report: {coverage_path}")
        
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
