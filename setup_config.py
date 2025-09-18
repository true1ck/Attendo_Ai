#!/usr/bin/env python3
"""
Setup Configuration
Automatically creates backend/config.py from template if it doesn't exist
"""

import os
import shutil
from pathlib import Path

def setup_backend_config():
    """Setup backend configuration if it doesn't exist"""
    
    backend_dir = Path(__file__).parent / "backend"
    config_file = backend_dir / "config.py"
    template_file = backend_dir / "config_template.py"
    
    print("🔧 Setting up backend configuration...")
    
    if config_file.exists():
        print("✅ backend/config.py already exists")
        return True
        
    if not template_file.exists():
        print("❌ backend/config_template.py not found")
        return False
        
    try:
        # Copy template to config.py
        shutil.copy2(template_file, config_file)
        print(f"✅ Created backend/config.py from template")
        
        # Update .gitignore to exclude the new config.py if not already there
        gitignore_file = Path(__file__).parent / ".gitignore"
        if gitignore_file.exists():
            gitignore_content = gitignore_file.read_text()
            if "backend/config.py" not in gitignore_content:
                with open(gitignore_file, "a") as f:
                    f.write("\n# Backend configuration (auto-generated)\nbackend/config.py\n")
                print("✅ Updated .gitignore to exclude backend/config.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating config file: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("ATTENDO - Configuration Setup")
    print("=" * 50)
    
    success = setup_backend_config()
    
    if success:
        print("\n✅ Configuration setup complete!")
        print("\n📋 Next steps:")
        print("   1. backend/config.py has been created from template")
        print("   2. Customize backend/config.py if needed")
        print("   3. Set environment variables for sensitive data")
        print("\n🚀 You can now run the application!")
    else:
        print("\n❌ Configuration setup failed!")
        print("\n🔧 Manual fix:")
        print("   1. Copy backend/config_template.py to backend/config.py")
        print("   2. Customize settings as needed")
    
    print("=" * 50)
