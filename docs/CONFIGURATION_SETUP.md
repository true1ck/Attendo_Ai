# Configuration Setup Guide

## Issue
When downloading the repository from GitHub, the `backend/config.py` file is missing because it's ignored by `.gitignore` (to protect sensitive configuration data).

## Quick Fix

### Option 1: Automatic Setup (Recommended)
Run the setup script:
```bash
python setup_config.py
```
This will automatically create `backend/config.py` from the template.

### Option 2: Manual Setup
1. Copy the template file:
   ```bash
   copy backend\config_template.py backend\config.py
   ```
   
2. Or on Linux/Mac:
   ```bash
   cp backend/config_template.py backend/config.py
   ```

### Option 3: Automatic on App Start
The main application (`app.py`) will automatically create the config file when you run it:
```bash
python app.py
```

## Configuration Details

### Default Configuration
The `config_template.py` provides safe defaults:
- **Database**: SQLite file (`vendor_timesheet.db`)
- **Security**: Default secret key (change in production!)
- **Notifications**: SMTP settings from environment variables
- **Sync**: Default intervals and settings

### Environment Variables
For production or sensitive data, use environment variables:
```bash
# Database
DATABASE_URL=your_database_url

# Security  
SECRET_KEY=your_secret_key

# Email/SMS
SMTP_USER=your_email@company.com
SMTP_PASSWORD=your_password
SMS_API_KEY=your_sms_key
```

### File Structure
```
backend/
├── config_template.py  ✅ (committed to git)
├── config.py          ❌ (ignored by git, auto-generated)
└── ...
```

## Troubleshooting

### Error: "No module named 'backend.config'"
**Solution**: Run one of the setup options above.

### Error: "ModuleNotFoundError: backend.config"
**Solution**: The config file is missing. Use the automatic setup:
```bash
python setup_config.py
```

### Custom Configuration Needed
1. Run the setup script to create the base config
2. Edit `backend/config.py` to customize settings
3. Set environment variables for sensitive data

## Security Notes

- `backend/config.py` is ignored by git to protect sensitive data
- Use environment variables for production secrets
- The template provides safe defaults for development
- Never commit actual API keys or passwords to git

## Next Steps After Setup

1. ✅ Configuration file created
2. 🔧 Customize settings in `backend/config.py` if needed  
3. 🔐 Set environment variables for sensitive data
4. 🚀 Run the application: `python app.py`

The application will now work properly with the billing corrections feature!
