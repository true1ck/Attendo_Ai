"""
Application Configuration Template
Copy this file to config.py and customize as needed
"""

import os
from pathlib import Path

class Config:
    """Base configuration"""
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'hackathon-attendo-vendor-timesheet-2025')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or f'sqlite:///{os.path.abspath("vendor_timesheet.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Notification Configuration
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    SMS_API_URL = os.getenv('SMS_API_URL')
    SMS_API_KEY = os.getenv('SMS_API_KEY')
    
    # Real-time sync configuration
    SYNC_INTERVAL_MINUTES = 5
    WEBHOOK_TIMEOUT_SECONDS = 30
    ENABLE_POWER_AUTOMATE_WEBHOOKS = True
    POWER_AUTOMATE_WEBHOOK_URLS = []
    SYNC_MONITORING_INTERVAL_MINUTES = 30
    SYNC_VALIDATION_INTERVAL_HOURS = 6
    ADMIN_EMAILS = ['admin@attendo.com']
    SYNC_ALERT_FROM = 'attendo-sync@attendo.com'
    
    # Excel Sync Configuration
    EXCEL_SYNC_ENABLED = True
    EXCEL_LOCAL_FOLDER = "notification_configs"
    EXCEL_NETWORK_FOLDER = None
    EXCEL_SYNC_INTERVAL = 600  # 10 minutes in seconds


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    DEVELOPMENT = True
    

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    DEVELOPMENT = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """Get configuration class based on config name"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])
