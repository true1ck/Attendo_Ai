"""
Mock Data Generator
==================

Generates realistic mock data for testing purposes.
"""

import random
import string
from datetime import datetime, date, time, timedelta
from typing import List, Dict, Any, Optional
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from models import (
    User, UserRole, Vendor, Manager, DailyStatus, 
    AttendanceStatus, ApprovalStatus, Holiday
)


class MockDataGenerator:
    """Generates realistic mock data for testing."""
    
    # Sample data pools
    FIRST_NAMES = [
        "John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona",
        "George", "Helen", "Ivan", "Julia", "Kevin", "Linda", "Michael", "Nancy",
        "Oliver", "Patricia", "Quinn", "Rachel", "Steve", "Tina", "Victor", "Wendy"
    ]
    
    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
    ]
    
    COMPANIES = [
        "TechSolutions Inc", "Global Systems Ltd", "Innovation Labs", 
        "Digital Dynamics", "Smart Solutions", "NextGen Technologies",
        "Alpha Systems", "Beta Corp", "Gamma Innovations", "Delta Tech"
    ]
    
    DEPARTMENTS = [
        "MTB_WCS_MSE7_MS1", "MTB_WCS_MSE7_MS2", "MTB_WCS_MSE7_MS3",
        "MTB_WCS_MSE8_MS1", "MTB_WCS_MSE8_MS2", "MTB_WCS_MSE9_MS1",
        "MTB_CAM_DEV_T1", "MTB_CAM_DEV_T2", "MTB_AI_ML_T1"
    ]
    
    LOCATIONS = [
        "BL-A-5F", "BL-A-6F", "BL-B-3F", "BL-B-4F", "BL-C-2F", 
        "BL-C-3F", "BL-D-1F", "BL-D-2F", "Campus-North", "Campus-South"
    ]
    
    BANDS = ["B1", "B2", "B3", "B4", "B5"]
    
    TEAM_NAMES = [
        "Alpha Team", "Beta Squad", "Gamma Group", "Delta Force",
        "Innovation Team", "Development Squad", "Quality Assurance Team",
        "Research Group", "Support Team", "Integration Team"
    ]
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize the mock data generator."""
        if seed:
            random.seed(seed)
        
        self._used_usernames = set()
        self._used_emails = set()
        self._used_vendor_ids = set()
        self._used_manager_ids = set()
    
    def generate_unique_username(self, base_name: Optional[str] = None) -> str:
        """Generate a unique username."""
        if base_name is None:
            base_name = f"{random.choice(self.FIRST_NAMES).lower()}.{random.choice(self.LAST_NAMES).lower()}"
        
        username = base_name
        counter = 1
        
        while username in self._used_usernames:
            username = f"{base_name}{counter}"
            counter += 1
        
        self._used_usernames.add(username)
        return username
    
    def generate_unique_email(self, username: Optional[str] = None, domain: str = "test.com") -> str:
        """Generate a unique email address."""
        if username is None:
            username = f"{random.choice(self.FIRST_NAMES).lower()}.{random.choice(self.LAST_NAMES).lower()}"
        
        email = f"{username}@{domain}"
        counter = 1
        
        while email in self._used_emails:
            email = f"{username}{counter}@{domain}"
            counter += 1
        
        self._used_emails.add(email)
        return email
    
    def generate_unique_vendor_id(self, prefix: str = "VDR") -> str:
        """Generate a unique vendor ID."""
        vendor_id = f"{prefix}{random.randint(1000, 9999)}"
        
        while vendor_id in self._used_vendor_ids:
            vendor_id = f"{prefix}{random.randint(1000, 9999)}"
        
        self._used_vendor_ids.add(vendor_id)
        return vendor_id
    
    def generate_unique_manager_id(self, prefix: str = "MGR") -> str:
        """Generate a unique manager ID."""
        manager_id = f"{prefix}{random.randint(100, 999)}"
        
        while manager_id in self._used_manager_ids:
            manager_id = f"{prefix}{random.randint(100, 999)}"
        
        self._used_manager_ids.add(manager_id)
        return manager_id
    
    def generate_phone_number(self) -> str:
        """Generate a random phone number."""
        return f"+1{random.randint(200, 999)}{random.randint(200, 999)}{random.randint(1000, 9999)}"
    
    def create_mock_user(self, role: UserRole = UserRole.VENDOR, **kwargs) -> Dict[str, Any]:
        """Create mock user data."""
        first_name = kwargs.get('first_name', random.choice(self.FIRST_NAMES))
        last_name = kwargs.get('last_name', random.choice(self.LAST_NAMES))
        
        username = kwargs.get('username', self.generate_unique_username(f"{first_name.lower()}.{last_name.lower()}"))
        email = kwargs.get('email', self.generate_unique_email(username))
        
        return {
            'username': username,
            'email': email,
            'password': kwargs.get('password', 'test123'),
            'role': role,
            'is_active': kwargs.get('is_active', True),
            'first_name': first_name,
            'last_name': last_name,
            'full_name': f"{first_name} {last_name}"
        }
    
    def create_mock_vendor(self, **kwargs) -> Dict[str, Any]:
        """Create mock vendor data."""
        vendor_data = self.create_mock_user(UserRole.VENDOR, **kwargs)
        
        return {
            **vendor_data,
            'vendor_id': kwargs.get('vendor_id', self.generate_unique_vendor_id()),
            'department': kwargs.get('department', random.choice(self.DEPARTMENTS)),
            'company': kwargs.get('company', random.choice(self.COMPANIES)),
            'band': kwargs.get('band', random.choice(self.BANDS)),
            'location': kwargs.get('location', random.choice(self.LOCATIONS))
        }
    
    def create_mock_manager(self, **kwargs) -> Dict[str, Any]:
        """Create mock manager data."""
        manager_data = self.create_mock_user(UserRole.MANAGER, **kwargs)
        
        return {
            **manager_data,
            'manager_id': kwargs.get('manager_id', self.generate_unique_manager_id()),
            'department': kwargs.get('department', random.choice(self.DEPARTMENTS)),
            'team_name': kwargs.get('team_name', random.choice(self.TEAM_NAMES)),
            'phone': kwargs.get('phone', self.generate_phone_number())
        }
    
    def create_mock_daily_status(
        self, 
        vendor_id: int,
        status_date: Optional[date] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create mock daily status data."""
        if status_date is None:
            status_date = date.today() - timedelta(days=random.randint(0, 30))
        
        # Generate realistic status based on day of week
        if status_date.weekday() >= 5:  # Weekend
            status = AttendanceStatus.LEAVE_FULL
        else:
            # Weighted random selection for weekdays
            status_choices = [
                (AttendanceStatus.IN_OFFICE_FULL, 60),
                (AttendanceStatus.WFH_FULL, 25),
                (AttendanceStatus.IN_OFFICE_HALF, 5),
                (AttendanceStatus.WFH_HALF, 5),
                (AttendanceStatus.LEAVE_FULL, 3),
                (AttendanceStatus.LEAVE_HALF, 2)
            ]
            
            status = random.choices(
                [s[0] for s in status_choices],
                weights=[s[1] for s in status_choices]
            )[0]
        
        # Generate realistic times
        start_hour = random.randint(8, 10)
        start_minute = random.choice([0, 15, 30, 45])
        in_time = time(start_hour, start_minute)
        
        if 'half' in status.value:
            work_hours = random.uniform(3.5, 4.5)
        else:
            work_hours = random.uniform(7.5, 9.0)
        
        out_time = (datetime.combine(status_date, in_time) + timedelta(hours=work_hours)).time()
        
        return {
            'vendor_id': vendor_id,
            'status_date': status_date,
            'status': status,
            'location': kwargs.get('location', 'Office' if 'office' in status.value else 'Home'),
            'in_time': in_time,
            'out_time': out_time,
            'total_hours': round(work_hours, 2),
            'comments': kwargs.get('comments', self.generate_random_comment(status)),
            'approval_status': kwargs.get('approval_status', ApprovalStatus.PENDING)
        }
    
    def generate_random_comment(self, status: AttendanceStatus) -> str:
        """Generate a random comment based on status."""
        comments_by_status = {
            AttendanceStatus.IN_OFFICE_FULL: [
                "Regular working day",
                "Team meeting scheduled",
                "Client presentation",
                "Project deadline work"
            ],
            AttendanceStatus.WFH_FULL: [
                "Working from home",
                "Focus work day",
                "Video conferences scheduled",
                "Remote collaboration"
            ],
            AttendanceStatus.LEAVE_FULL: [
                "Sick leave",
                "Personal leave",
                "Vacation day",
                "Family emergency"
            ],
            AttendanceStatus.IN_OFFICE_HALF: [
                "Half day - morning office",
                "Half day - afternoon office",
                "Medical appointment"
            ],
            AttendanceStatus.WFH_HALF: [
                "Half day - remote work",
                "Morning WFH session",
                "Afternoon remote meeting"
            ],
            AttendanceStatus.LEAVE_HALF: [
                "Half day leave",
                "Personal appointment",
                "Family commitment"
            ]
        }
        
        return random.choice(comments_by_status.get(status, ["Standard work day"]))
    
    def create_mock_holiday(self, holiday_date: date, **kwargs) -> Dict[str, Any]:
        """Create mock holiday data."""
        holiday_names = [
            "New Year's Day", "Independence Day", "Christmas Day",
            "Thanksgiving", "Labor Day", "Memorial Day",
            "Good Friday", "Easter Monday", "Diwali", "Eid"
        ]
        
        return {
            'holiday_date': holiday_date,
            'name': kwargs.get('name', random.choice(holiday_names)),
            'description': kwargs.get('description', 'Official company holiday'),
            'created_by': kwargs.get('created_by', 1)  # Admin user ID
        }
    
    def create_realistic_work_pattern(
        self, 
        vendor_id: int, 
        start_date: date, 
        days: int
    ) -> List[Dict[str, Any]]:
        """Create a realistic work pattern over a period."""
        statuses = []
        current_date = start_date
        
        for _ in range(days):
            # Skip some weekend days (not all companies work weekends)
            if current_date.weekday() >= 5:  # Weekend
                if random.random() > 0.1:  # 90% chance to skip weekend
                    current_date += timedelta(days=1)
                    continue
            
            # Create occasional leave patterns
            if random.random() < 0.05:  # 5% chance of leave
                status_data = self.create_mock_daily_status(
                    vendor_id, 
                    current_date, 
                    status=AttendanceStatus.LEAVE_FULL
                )
            else:
                status_data = self.create_mock_daily_status(vendor_id, current_date)
            
            statuses.append(status_data)
            current_date += timedelta(days=1)
        
        return statuses
    
    def create_team_data(self, team_size: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """Create data for an entire team including manager and vendors."""
        # Create manager
        manager_data = self.create_mock_manager()
        
        # Create vendors for this manager
        vendors_data = []
        for _ in range(team_size):
            vendor_data = self.create_mock_vendor(
                department=manager_data['department']
            )
            vendors_data.append(vendor_data)
        
        return {
            'manager': manager_data,
            'vendors': vendors_data
        }
    
    def reset(self):
        """Reset all used identifiers."""
        self._used_usernames.clear()
        self._used_emails.clear()
        self._used_vendor_ids.clear()
        self._used_manager_ids.clear()
