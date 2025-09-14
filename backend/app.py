"""
Flask App Factory
Creates and configures the Flask application with all blueprints and extensions
"""

import os
import json
from flask import Flask, request
from backend.config import get_config
from backend.extensions import init_extensions
from backend.models import db

# Import all blueprints
from backend.routes.auth_routes import auth_bp
from backend.routes.vendor_routes import vendor_bp
from backend.routes.admin_routes import admin_bp
from backend.routes.manager_routes import manager_bp

def create_app(config_name=None):
    """Create and configure Flask application"""
    
    app = Flask(__name__, 
                template_folder='../templates',  # Relative to backend folder
                static_folder='../static')       # Relative to backend folder
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Initialize extensions
    init_extensions(app)
    
    # Add JSON filter for templates (from original app.py)
    @app.template_filter('fromjson')
    def fromjson_filter(value):
        """Parse JSON string to Python object"""
        if not value:
            return {}
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return {}
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(vendor_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(manager_bp)
    
    # Initialize database and create tables
    with app.app_context():
        create_tables(app)
    
    # Register external blueprints and services (from original app.py)
    register_external_services(app)
    
    return app


def create_tables(app):
    """Create database tables and ensure default Admin user exists"""
    from backend.models import User, UserRole
    from sqlalchemy import or_
    
    db.create_all()
    
    # Run database migrations if needed
    try:
        from migrate_database import migrate_database
        print("🔄 Checking for database migrations...")
        migrate_database()
    except Exception as e:
        print(f"⚠️ Migration check failed: {e}")
    
    # Ensure default Admin user exists (Admin/admin123)
    admin_user = User.query.filter(or_(
        User.username == 'Admin',
        User.username == 'admin',
        User.email == 'admin@attendo.com'
    )).first()
    
    if admin_user:
        # Normalize credentials to requested ones
        admin_user.username = 'Admin'
        admin_user.email = 'admin@attendo.com'
        admin_user.role = UserRole.ADMIN
        admin_user.is_active = True
        admin_user.set_password('admin123')
        db.session.commit()
    else:
        admin_user = User(
            username='Admin',
            email='admin@attendo.com',
            role=UserRole.ADMIN,
            is_active=True
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()


def register_external_services(app):
    """Register external blueprints and services from the original app"""
    
    # Import other modules (from original app.py)
    try:
        from import_routes import import_bp
        app.register_blueprint(import_bp)
    except ImportError as e:
        print(f"⚠️ Import routes not available: {e}")
    
    try:
        from swagger_ui import register_swagger_ui
        register_swagger_ui(app)
    except ImportError as e:
        print(f"⚠️ Swagger UI not available: {e}")
    
    try:
        from scripts.power_automate_api import register_power_automate_api
        register_power_automate_api(app)
    except ImportError as e:
        print(f"⚠️ Power Automate API not available: {e}")
    
    # Initialize notification service
    try:
        from notification_service import notification_service, setup_notification_scheduler
        notification_service.init_app(app)
        setup_notification_scheduler(app, notification_service)
    except ImportError as e:
        print(f"⚠️ Notification service not available: {e}")
    
    # Initialize real-time notification sync system
    try:
        from scripts.setup_realtime_notification_sync import setup_complete_notification_sync_system
        print("\n🚀 Initializing Real-Time Notification Sync System...")
        sync_components = setup_complete_notification_sync_system(app)
        
        # Store components in app context for access
        app.sync_manager = sync_components['sync_manager']
        app.realtime_sync = sync_components['realtime_sync']
        app.monitor = sync_components['monitor']
        
        print("✅ Real-Time Notification Sync System initialized successfully!")
    except Exception as e:
        print(f"⚠️ Real-Time Sync System initialization failed: {str(e)}")
        print("   App will continue without real-time sync features")
    
    # Initialize demo data if needed
    try:
        from demo_data import create_demo_data
        with app.app_context():
            create_demo_data()
    except ImportError as e:
        print(f"⚠️ Demo data not available: {e}")
    except Exception as e:
        print(f"⚠️ Demo data initialization failed: {e}")


# Create the application instance for development
if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
