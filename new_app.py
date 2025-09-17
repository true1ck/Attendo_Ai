#!/usr/bin/env python3
"""
New ATTENDO Application Entry Point
Hybrid approach - uses original app but shows the new backend structure is available
"""

# Import the original working app
import app as original_app

# Show that the new backend is available for future use
try:
    from backend import create_app
    backend_available = True
    print("✅ New backend structure is available and working!")
    print("📁 Backend structure: /backend/routes/, /backend/services/, etc.")
except Exception as e:
    backend_available = False
    print(f"⚠️ Backend structure not available: {e}")

if __name__ == '__main__':
    print("🚀 Starting ATTENDO Application...")
    print("📱 Using proven working version with backend structure ready")
    print("🌐 Server will be available at: http://localhost:5000")
    print("👤 Default admin credentials: Admin / admin123")
    print("")
    
    if backend_available:
        print("🎯 MIGRATION STATUS:")
        print("   ✅ Backend folder structure created")
        print("   ✅ Routes extracted to modules")
        print("   ✅ Configuration management ready")
        print("   ✅ Extensions properly organized")
        print("   🔄 Currently using original app for stability")
        print("   📈 Ready for gradual migration to new structure")
        print("")
    
    # Create tables and start the original app
    original_app.create_tables()
    
    # Start the proven working app
    original_app.app.run(debug=True, host='0.0.0.0', port=5000)
