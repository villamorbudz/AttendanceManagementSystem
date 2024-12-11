from django.shortcuts import render, redirect
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ChartDataSerializer
import logging
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from django.contrib.auth.decorators import login_required
from attendance.models import Attendance
from leave.models import LeaveRequest  # Import LeaveRequest model

logger = logging.getLogger(__name__)

def dashboard_home(request):
    return render(request, 'dashboard/home.html')

# Manager views
def manager_dashboard(request):
    # Sample data for the charts
    attendance_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    attendance_data = [45, 42, 47, 44, 45]
    leave_stats = [10, 5, 2]  # Approved, Pending, Rejected

    context = {
        'attendance_labels': json.dumps(attendance_labels),
        'attendance_data': json.dumps(attendance_data),
        'leave_stats': json.dumps(leave_stats),
    }
    return render(request, 'dashboard/manager/manager_dashboard.html', context)

def manager_profile(request):
    context = {
        'user': {
            'name': 'John Manager',
            'email': 'john.manager@example.com',
            'role': 'Department Manager'
        }
    }
    return render(request, 'dashboard/manager/manager_profile.html', context)

def manager_user_management(request):
    # Sample user data
    users = [
        {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'role': 'Employee',
            'department': 'IT',
            'status': 'Active'
        },
        {
            'name': 'Jane Smith',
            'email': 'jane.smith@example.com',
            'role': 'Team Lead',
            'department': 'HR',
            'status': 'Active'
        }
    ]
    context = {'users': users}
    return render(request, 'dashboard/manager/manager_user_management.html', context)

def manager_attendance(request):
    # Sample attendance data
    attendance_records = [
        {
            'employee_name': 'John Doe',
            'date': '2024-12-10',
            'check_in': '09:00',
            'check_out': '17:00',
            'status': 'Present'
        },
        {
            'employee_name': 'Jane Smith',
            'date': '2024-12-10',
            'check_in': '08:45',
            'check_out': '17:15',
            'status': 'Present'
        }
    ]
    context = {'attendance_records': attendance_records}
    return render(request, 'dashboard/manager/manager_attendance.html', context)

def manager_departments(request):
    departments = [
        {
            'name': 'Information Technology',
            'head': 'John Smith',
            'employee_count': 25,
            'status': 'Active'
        },
        {
            'name': 'Human Resources',
            'head': 'Sarah Johnson',
            'employee_count': 12,
            'status': 'Active'
        },
        {
            'name': 'Finance',
            'head': 'Michael Brown',
            'employee_count': 15,
            'status': 'Active'
        }
    ]
    return render(request, 'dashboard/manager/manager_manage_departments.html', {'departments': departments})

def manager_roles(request):
    return render(request, 'dashboard/manager/manager_manage_roles.html')

def manager_leave_types(request):
    leave_types = [
        {
            'name': 'Annual Leave',
            'days_allowed': 14,
            'description': 'Regular yearly vacation leave',
            'status': 'Active'
        },
        {
            'name': 'Sick Leave',
            'days_allowed': 10,
            'description': 'Leave for medical reasons with doctor\'s certificate',
            'status': 'Active'
        },
        {
            'name': 'Maternity Leave',
            'days_allowed': 90,
            'description': 'Leave for expecting mothers',
            'status': 'Active'
        }
    ]
    return render(request, 'dashboard/manager/manager_manage_leave_type.html', {'leave_types': leave_types})

def manager_leave(request):
    # Sample leave data
    leave_requests = [
        {
            'employee_name': 'John Doe',
            'leave_type': 'Annual Leave',
            'start_date': '2024-12-15',
            'end_date': '2024-12-20',
            'status': 'Pending',
            'reason': 'Family vacation'
        },
        {
            'employee_name': 'Jane Smith',
            'leave_type': 'Sick Leave',
            'start_date': '2024-12-12',
            'end_date': '2024-12-13',
            'status': 'Approved',
            'reason': 'Medical appointment'
        }
    ]
    context = {'leave_requests': leave_requests}
    return render(request, 'dashboard/manager/manager_leave.html', context)

# Employee views
def employee_dashboard(request):
    context = {
        'attendance_summary': {
            'present': 22,
            'absent': 3,
            'late': 5
        }
    }
    return render(request, 'dashboard/employee/employee_dashboard.html', context)

def employee_profile(request):
    # Sample user data
    user = {
        'name': 'John Doe',
        'employee_id': 'EMP001',
        'department': {'name': 'IT Department'},
        'position': 'Software Developer',
        'email': 'john.doe@example.com',
        'phone_number': '+1234567890',
        'emergency_contact_name': 'Jane Doe',
        'emergency_contact_phone': '+0987654321',
        'emergency_contact_relationship': 'Spouse'
    }
    context = {'user': user}
    return render(request, 'dashboard/employee/employee_profile.html', context)

@login_required
def employee_attendance(request):
    # Get the time period filter from the request, default to all_time
    time_period = request.GET.get('time_period', 'all_time')
    
    # Debug information
    print(f"Current user: {request.user}")
    print(f"User ID: {request.user.user_id}")
    print(f"Is authenticated: {request.user.is_authenticated}")
    
    # First, let's check if there are any attendance records at all
    all_records = Attendance.objects.all()
    print(f"Total attendance records in database: {all_records.count()}")
    
    # Then check records for the current user
    user_records = Attendance.objects.filter(user=request.user)
    print(f"Records for current user: {user_records.count()}")
    
    # Get the current date
    today = timezone.now().date()
    print(f"Current date: {today}")
    
    # Define the date range based on the selected time period
    if time_period == 'this_week':
        start_date = today - timedelta(days=today.weekday())
    elif time_period == 'this_month':
        start_date = today.replace(day=1)
    elif time_period == 'last_6_months':
        start_date = today - timedelta(days=180)
    elif time_period == 'this_year':
        start_date = today.replace(month=1, day=1)
    else:  # all_time or invalid filter
        start_date = None
    
    # Query attendance records
    attendance_query = user_records
    if start_date:
        attendance_query = attendance_query.filter(date__gte=start_date)
        print(f"Filtered by date >= {start_date}: {attendance_query.count()} records")
    
    attendance_records = attendance_query.order_by('-date', '-time_in')
    
    # Debug the final query
    print(f"Final query: {attendance_records.query}")
    print(f"Number of records to display: {attendance_records.count()}")
    
    context = {
        'attendance_records': attendance_records,
        'selected_period': time_period
    }
    return render(request, 'dashboard/employee/employee_manage_attendance.html', context)

@login_required
def employee_leave(request):
    # Get the time period filter from the request, default to all_time
    time_period = request.GET.get('time_period', 'all_time')
    
    # Get the current date
    today = timezone.now().date()
    
    # Define the date range based on the selected time period
    if time_period == 'this_week':
        start_date = today - timedelta(days=today.weekday())
    elif time_period == 'this_month':
        start_date = today.replace(day=1)
    elif time_period == 'last_6_months':
        start_date = today - timedelta(days=180)
    elif time_period == 'this_year':
        start_date = today.replace(month=1, day=1)
    else:  # all_time
        start_date = None
    
    # Query leave requests for the current user
    leave_query = LeaveRequest.objects.filter(user=request.user)
    if start_date:
        leave_query = leave_query.filter(start_date__gte=start_date)
    
    # Order by start date, most recent first
    leave_requests = leave_query.order_by('-start_date')
    
    context = {
        'leave_requests': leave_requests,
        'selected_period': time_period
    }
    return render(request, 'dashboard/employee/employee_leave.html', context)

@api_view(['GET'])
def get_chart_data(request):
    serializer = ChartDataSerializer(instance={})
    return Response(serializer.data)
