"""
Flask Extensions Initialization
Handles all Flask extensions to avoid circular imports
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Import the existing db instance from models to avoid conflicts
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from models import db

# Initialize login manager
login_manager = LoginManager()

def init_extensions(app):
    """Initialize Flask extensions with the app instance"""
    
    # Initialize SQLAlchemy
    db.init_app(app)
    
    # Initialize Login Manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Updated to use blueprint
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Import and register user_loader after app context is available
    with app.app_context():
        from backend.models import User
        
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
    
    return app
