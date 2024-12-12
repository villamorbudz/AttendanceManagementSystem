import os
import django
import sys
from datetime import timedelta

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AMSystem.settings')
django.setup()

from django.utils import timezone
from django.contrib.auth import get_user_model
from attendance.models import Attendance
from management.models import Department

User = get_user_model()
today = timezone.now().date()
yesterday = today - timedelta(days=1)

# Create a test department
department, _ = Department.objects.get_or_create(
    name='Test Department'
)

# Get or create test users
for i in range(1, 11):
    user, created = User.objects.get_or_create(
        email=f'testuser{i}@example.com',
        defaults={
            'first_name': f'Test{i}',
            'last_name': 'User',
            'contact_number': f'123456789{i}',
            'birthdate': '1990-01-01',
            'department': department,
            'user_id': f'EMP{i:03d}'
        }
    )
    
    # Create today's attendance
    if i <= 7:  # 7 present today
        status = 'Present'
    else:  # 3 absent today
        status = 'Absent'
        
    Attendance.objects.update_or_create(
        user=user,
        date=today,
        defaults={
            'status': status,
            'time_in': '09:00',
            'time_out': '17:00'
        }
    )
    
    # Create yesterday's attendance
    if i <= 5:  # 5 present yesterday
        status = 'Present'
    else:  # 5 absent yesterday
        status = 'Absent'
        
    Attendance.objects.update_or_create(
        user=user,
        date=yesterday,
        defaults={
            'status': status,
            'time_in': '09:00',
            'time_out': '17:00'
        }
    )

print("Test data has been added successfully!")
