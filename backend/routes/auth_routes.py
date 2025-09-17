"""
Authentication Routes
Handles login, logout, and authentication-related functionality
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from backend.models import User, UserRole
from backend.extensions import db
from backend.utils.helpers import create_audit_log

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    """Home page - redirect to appropriate dashboard based on user role"""
    if current_user.is_authenticated:
        if current_user.role == UserRole.VENDOR:
            return redirect(url_for('vendor.dashboard'))
        elif current_user.role == UserRole.MANAGER:
            return redirect(url_for('manager.dashboard'))
        elif current_user.role == UserRole.ADMIN:
            return redirect(url_for('admin.dashboard'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login with clear feedback for common errors"""
    prefill_username = ''
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = (request.form.get('password') or '').strip()
        prefill_username = username

        # Basic validation
        if not username and not password:
            flash('Please enter your username and password.', 'warning')
            return render_template('login.html', prefill_username=prefill_username)
        if not username:
            flash('Please enter your username.', 'warning')
            return render_template('login.html', prefill_username=prefill_username)
        if not password:
            flash('Please enter your password.', 'warning')
            return render_template('login.html', prefill_username=prefill_username)

        # Find user by username (or email fallback if needed later)
        user = User.query.filter_by(username=username).first()

        if not user:
            flash('User not found. Please check your username.', 'error')
            return render_template('login.html', prefill_username=prefill_username)

        if not user.is_active:
            flash('Your account is disabled. Please contact the administrator.', 'error')
            return render_template('login.html', prefill_username=prefill_username)
        
        if not user.check_password(password):
            flash('Incorrect password. Please try again.', 'error')
            return render_template('login.html', prefill_username=prefill_username)

        # Success
        login_user(user)
        user.last_login = datetime.utcnow()
        db.session.commit()
        create_audit_log(user.id, 'LOGIN', 'users', user.id, {}, {'last_login': str(datetime.utcnow())})
        flash(f'Welcome {user.username}!', 'success')
        return redirect(url_for('auth.index'))
    
    return render_template('login.html', prefill_username=prefill_username)


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    create_audit_log(current_user.id, 'LOGOUT', 'users', current_user.id, {}, {})
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))
