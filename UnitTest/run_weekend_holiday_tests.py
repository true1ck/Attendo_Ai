#!/usr/bin/env python3
"""
Weekend/Holiday Exclusion Test Runner
====================================

This script runs the weekend and holiday exclusion tests using the proper
project structure and imports.
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Main test runner function"""
    print("🧪 Weekend/Holiday Exclusion Test Runner")
    print("=" * 50)
    
    # Get the current directory (UnitTest)
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    
    print(f"📁 UnitTest Directory: {current_dir}")
    print(f"📁 Project Root: {project_root}")
    
    # Add project root to Python path
    sys.path.insert(0, str(project_root))
    
    print("\n🔄 Running standalone test suite...")
    
    try:
        # Import and run the standalone test
        from test_weekend_holiday_exclusion_standalone import run_all_tests
        
        success = run_all_tests()
        
        if success:
            print("\n🎉 All weekend/holiday exclusion tests passed!")
            return 0
        else:
            print("\n❌ Some tests failed.")
            return 1
            
    except ImportError as e:
        print(f"❌ Failed to import test module: {e}")
        return 1
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
