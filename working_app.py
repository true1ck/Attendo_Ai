#!/usr/bin/env python3
"""
Working ATTENDO Application
This version guarantees to work by using the original app structure
"""

# Import the original working app
import app

def main():
    """Main entry point for the working application"""
    print("🚀 Starting ATTENDO Application...")
    print("📊 Using proven working version")
    print("🌐 Server will be available at: http://localhost:5000")
    print("👤 Default admin credentials: Admin / admin123")
    print("")
    
    # Show available routes
    routes = []
    for rule in app.app.url_map.iter_rules():
        routes.append(f"   {rule.methods} {rule.rule}")
    
    print(f"📍 Available routes ({len(routes)} total):")
    # Show first 10 routes to avoid clutter
    for route in sorted(routes)[:10]:
        print(route)
    if len(routes) > 10:
        print(f"   ... and {len(routes) - 10} more routes")
    print("")
    
    # Create tables
    print("🗄️ Initializing database...")
    app.create_tables()
    
    print("✅ Application ready!")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("▶️ Starting server...")
    print("")
    
    # Start the application
    app.app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
