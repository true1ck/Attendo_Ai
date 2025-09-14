#!/usr/bin/env python3
"""
New ATTENDO Application Entry Point
Hybrid approach - uses original app but shows the new backend structure is available
"""

# Import the original working app
import app as original_app

# Check if the new backend is available for future development
try:
    from backend.app import create_app
    backend_available = True
    print("✅ New backend structure is available for future development")
    print("📁 Backend structure: /backend/routes/, /backend/services/, etc.")
except Exception as e:
    backend_available = False
    print(f"⚠️ Backend structure not available: {e}")

if __name__ == '__main__':
    print("🚀 Starting ATTENDO Application...")
    print("📱 Using complete working version with all features")
    print("")
    print("🌐 MAIN APPLICATION: http://localhost:5000")
    print("📚 API Documentation: http://localhost:5000/api/docs")
    print("")
    print("👤 Default admin credentials: Admin / admin123")
    print("")
    
    print("🎯 FEATURES AVAILABLE:")
    print("   ✅ Complete attendance management system")
    print("   ✅ All admin, manager, and vendor dashboards")
    print("   ✅ Excel notification sync system (10-min intervals)")
    print("   ✅ Power Automate integration ready")
    print("   ✅ AI insights and analytics")
    print("   ✅ Import/Export functionality")
    print("   ✅ Comprehensive API endpoints")
    
    if backend_available:
        print("\n🔧 DEVELOPMENT STATUS:")
        print("   ✅ Backend folder structure created")
        print("   ⚠️ Backend routes incomplete (55+ routes missing)")
        print("   🔄 Currently using complete original app")
        print("   📈 Backend available for future development")
    print("")
    
    # Create tables and start the original app
    original_app.create_tables()
    
    print("✅ Database initialized successfully!")
    print("⚡ Starting server...")
    print("")
    print("📌 IMPORTANT: Open your browser and go to:")
    print("     🌐 Main App: http://localhost:5000 (NOT /api/docs)")
    print("     👤 Login with: Admin / admin123")
    print("")
    
    # Start the proven working app
    original_app.app.run(debug=True, host='0.0.0.0', port=5000)
