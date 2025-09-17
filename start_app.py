#!/usr/bin/env python3
"""
ATTENDO Application Startup Script
Starts the application on port 5001 to avoid conflicts
"""

from app import app

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 Starting ATTENDO Application")
    print("="*70)
    print("📍 URL: http://localhost:5001")
    print("📚 API Docs: http://localhost:5001/api/docs") 
    print("👤 Login: Admin / admin123")
    print("="*70)
    
    app.run(host='0.0.0.0', port=5001, debug=True)
