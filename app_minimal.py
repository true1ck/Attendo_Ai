#!/usr/bin/env python3
"""
Minimal Working ATTENDO Application
Test version to ensure basic functionality works
"""

from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hackathon-attendo-vendor-timesheet-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath("vendor_timesheet.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import models first to get the correct db instance
import models
from models import User, UserRole

# Initialize extensions with the existing db instance
db = models.db
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    """Home page - redirect to login or appropriate dashboard"""
    if current_user.is_authenticated:
        if current_user.role == UserRole.VENDOR:
            return f"<h1>Welcome {current_user.username}!</h1><p>Vendor Dashboard would be here</p><a href='/logout'>Logout</a>"
        elif current_user.role == UserRole.MANAGER:
            return f"<h1>Welcome {current_user.username}!</h1><p>Manager Dashboard would be here</p><a href='/logout'>Logout</a>"
        elif current_user.role == UserRole.ADMIN:
            return f"<h1>Welcome {current_user.username}!</h1><p>Admin Dashboard would be here</p><a href='/logout'>Logout</a>"
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Simple login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Please enter both username and password.', 'warning')
            return render_login_form(username)
        
        user = User.query.filter_by(username=username).first()
        
        if not user:
            flash('User not found.', 'error')
            return render_login_form(username)
        
        if not user.is_active:
            flash('Account is disabled.', 'error')
            return render_login_form(username)
        
        if not user.check_password(password):
            flash('Incorrect password.', 'error')
            return render_login_form(username)
        
        login_user(user)
        user.last_login = datetime.utcnow()
        db.session.commit()
        flash(f'Welcome {user.username}!', 'success')
        return redirect(url_for('index'))
    
    return render_login_form()

def render_login_form(username=''):
    """Render login form (inline HTML for simplicity)"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ATTENDO Login</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 400px; margin: 100px auto; padding: 20px; }}
            .form-group {{ margin: 15px 0; }}
            label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
            input {{ width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }}
            button {{ width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }}
            button:hover {{ background: #0056b3; }}
            .alert {{ padding: 10px; margin: 10px 0; border-radius: 4px; }}
            .alert-success {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
            .alert-error {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
            .alert-warning {{ background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }}
            .logo {{ text-align: center; margin-bottom: 30px; }}
            .logo h1 {{ color: #007bff; margin: 0; }}
            .logo p {{ color: #666; margin: 5px 0; }}
        </style>
    </head>
    <body>
        <div class="logo">
            <h1>🎯 ATTENDO</h1>
            <p>Workforce Management System</p>
        </div>
        
        {''.join([f'<div class="alert alert-{category}">{message}</div>' for category, message in get_flashed_messages(with_categories=True)])}
        
        <form method="POST">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" value="{username}" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit">Login</button>
        </form>
        
        <div style="margin-top: 20px; text-align: center; color: #666; font-size: 12px;">
            <p>Default Admin: <strong>Admin / admin123</strong></p>
        </div>
    </body>
    </html>
    """

@app.route('/logout')
@login_required
def logout():
    """Simple logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

def create_tables():
    """Create database tables and ensure default Admin user exists"""
    with app.app_context():
        db.create_all()
        
        # Ensure default Admin user exists
        from sqlalchemy import or_
        admin_user = User.query.filter(or_(
            User.username == 'Admin',
            User.username == 'admin',
            User.email == 'admin@attendo.com'
        )).first()
        
        if admin_user:
            # Update existing admin
            admin_user.username = 'Admin'
            admin_user.email = 'admin@attendo.com'
            admin_user.role = UserRole.ADMIN
            admin_user.is_active = True
            admin_user.set_password('admin123')
            db.session.commit()
            print("✅ Updated existing admin user")
        else:
            # Create new admin
            admin_user = User(
                username='Admin',
                email='admin@attendo.com',
                role=UserRole.ADMIN,
                is_active=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Created new admin user")

if __name__ == '__main__':
    print("🚀 Starting Minimal ATTENDO Application...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("👤 Default admin credentials: Admin / admin123")
    print("")
    
    # Create tables
    create_tables()
    
    print("✅ Database initialized")
    print("▶️ Starting server...")
    
    # Start the app
    app.run(debug=True, host='0.0.0.0', port=5000)
