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
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from management.models import User, Role, Department  # Import from management app

logger = logging.getLogger(__name__)

def dashboard_home(request):
    return render(request, 'dashboard/home.html')

# Manager views
@login_required
def manager_dashboard(request):
    today = timezone.now().date()
    
    # Get active employees today
    active_employees = Attendance.objects.filter(
        date=today,
        status__in=['Present', 'Working']
    ).count()

    # Get present and absent counts
    present_employees = Attendance.objects.filter(
        date=today,
        status='Present'
    ).count()
    
    absent_employees = Attendance.objects.filter(
        date=today,
        status='Absent'
    ).count()

    # Calculate trends for present and absent
    yesterday = today - timedelta(days=1)
    
    yesterday_present = Attendance.objects.filter(
        date=yesterday,
        status='Present'
    ).count()
    
    yesterday_absent = Attendance.objects.filter(
        date=yesterday,
        status='Absent'
    ).count()

    # Calculate weekly attendance data
    weekly_data = []
    for i in range(7):
        date = today - timedelta(days=i)
        present_count = Attendance.objects.filter(date=date, status='Present').count()
        absent_count = Attendance.objects.filter(date=date, status='Absent').count()
        weekly_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'present': present_count,
            'absent': absent_count
        })
    
    weekly_data.reverse()  # Show oldest to newest

    # Calculate trends
    if yesterday_present > 0:
        present_trend = ((present_employees - yesterday_present) / yesterday_present) * 100
    else:
        present_trend = 100 if present_employees > 0 else 0

    if yesterday_absent > 0:
        absent_trend = ((absent_employees - yesterday_absent) / yesterday_absent) * 100
    else:
        absent_trend = 100 if absent_employees > 0 else 0

    # Get pending leave count
    pending_leave_count = LeaveRequest.objects.filter(status='pending').count()

    context = {
        'active_employees': active_employees,
        'present_employees': present_employees,
        'absent_employees': absent_employees,
        'present_trend': present_trend,
        'absent_trend': absent_trend,
        'weekly_data': weekly_data,
        'weekly_labels': [day['date'] for day in weekly_data],
        'weekly_present': [day['present'] for day in weekly_data],
        'weekly_absent': [day['absent'] for day in weekly_data],
        'pending_leave_count': pending_leave_count
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
    # Get filter parameters
    department_filter = request.GET.get('department')
    role_filter = request.GET.get('role')
    search_query = request.GET.get('search')
    per_page = request.GET.get('per_page', 10)  # Default to 10 items per page
    
    try:
        per_page = int(per_page)
        if per_page not in [10, 25, 50, 100]:
            per_page = 10
    except (ValueError, TypeError):
        per_page = 10
    
    # Start with all users
    users_list = User.objects.select_related('department').all()
    
    # Apply filters
    if department_filter and department_filter != 'all':
        try:
            users_list = users_list.filter(department_id=int(department_filter))
        except (ValueError, TypeError):
            department_filter = 'all'
    
    if role_filter and role_filter != 'all':
        try:
            role = Role.objects.get(id=int(role_filter))
            users_list = users_list.filter(department__role=role)
        except (Role.DoesNotExist, ValueError, TypeError):
            role_filter = 'all'
    
    if search_query:
        users_list = users_list.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(user_id__icontains=search_query)
        )
    
    # Order by name
    users_list = users_list.order_by('first_name', 'last_name')
    
    # Pagination
    paginator = Paginator(users_list, per_page)
    page = request.GET.get('page', 1)
    
    try:
        page = int(page)
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1
    
    try:
        users = paginator.page(page)
    except Paginator.PageNotAnInteger:
        users = paginator.page(1)
    except Paginator.EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    # Calculate visible page range
    page_range = []
    current_page = users.number
    total_pages = paginator.num_pages

    # Always show first page, last page, and pages around current page
    if total_pages <= 7:
        page_range = range(1, total_pages + 1)
    else:
        # Always include first and last page
        if current_page <= 4:
            page_range = list(range(1, 6)) + ['...', total_pages]
        elif current_page >= total_pages - 3:
            page_range = [1, '...'] + list(range(total_pages - 4, total_pages + 1))
        else:
            page_range = [1, '...'] + list(range(current_page - 1, current_page + 2)) + ['...', total_pages]
    
    # Get departments and roles for filters
    departments = Department.objects.all()
    roles = Role.objects.all()
    
    context = {
        'users': users,
        'departments': departments,
        'roles': roles,
        'total_users': paginator.count,
        'total_pages': total_pages,
        'page_range': page_range,
        'current_page': current_page,
        'per_page': per_page,
        'current_filters': {
            'department': department_filter or 'all',
            'role': role_filter or 'all',
            'search': search_query or ''
        }
    }
    
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
    # Get all departments from the database
    departments_list = Department.objects.all().order_by('name')
    
    # Number of departments per page
    per_page = 10
    
    # Create a paginator instance
    paginator = Paginator(departments_list, per_page)
    
    # Get the current page number from the request's GET parameters
    page = request.GET.get('page', 1)
    
    try:
        # Get the Page object for the requested page
        departments = paginator.page(page)
    except Paginator.PageNotAnInteger:
        # If page is not an integer, deliver first page
        departments = paginator.page(1)
    except Paginator.EmptyPage:
        # If page is out of range, deliver last page of results
        departments = paginator.page(paginator.num_pages)
    
    return render(request, 'dashboard/manager/manager_manage_departments.html', {
        'departments': departments,
        'total_departments': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': int(page)
    })

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

@login_required
def manager_leave_requests(request):
    # Get all leave requests with related data
    leave_requests_list = LeaveRequest.objects.select_related(
        'user', 'department', 'leave_type'
    ).order_by('-created_at')
    
    # Apply filters if provided
    status_filter = request.GET.get('status')
    date_filter = request.GET.get('date')
    department_filter = request.GET.get('department')
    
    if status_filter and status_filter != 'all':
        leave_requests_list = leave_requests_list.filter(status=status_filter)
    if date_filter:
        leave_requests_list = leave_requests_list.filter(start_date__lte=date_filter, end_date__gte=date_filter)
    if department_filter and department_filter != 'all':
        leave_requests_list = leave_requests_list.filter(department_id=department_filter)
    
    # Number of leave requests per page
    per_page = 10
    paginator = Paginator(leave_requests_list, per_page)
    page = request.GET.get('page', 1)
    
    try:
        leave_requests = paginator.page(page)
    except Paginator.PageNotAnInteger:
        leave_requests = paginator.page(1)
    except Paginator.EmptyPage:
        leave_requests = paginator.page(paginator.num_pages)
    
    # Get all departments for the filter
    departments = Department.objects.all()
    
    context = {
        'leave_requests': leave_requests,
        'departments': departments,
        'total_requests': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': int(page),
        'current_filters': {
            'status': status_filter or 'all',
            'date': date_filter or '',
            'department': department_filter or 'all'
        }
    }
    
    return render(request, 'dashboard/manager/manager_leave_requests.html', context)

@login_required
def process_leave_request(request, request_id, action):
    if not request.user.is_manager:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    try:
        leave_request = LeaveRequest.objects.get(id=request_id)
        
        if action == 'approve':
            leave_request.status = 'approved'
        elif action == 'reject':
            leave_request.status = 'rejected'
        else:
            return JsonResponse({'success': False, 'message': 'Invalid action'}, status=400)
        
        leave_request.processed_by = request.user
        leave_request.processed_at = timezone.now()
        leave_request.save()

        return JsonResponse({'success': True})
    except LeaveRequest.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Leave request not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

# Employee views
@login_required
def employee_dashboard(request):
    today = timezone.now().date()
    user = request.user

    # Get today's attendance for the user
    today_attendance = Attendance.objects.filter(
        user=user,
        date=today
    ).first()

    # Calculate total present days for the user
    total_present = Attendance.objects.filter(
        user=user,
        status='Present'
    ).count()

    # Calculate attendance trend
    yesterday = today - timedelta(days=1)
    yesterday_present = Attendance.objects.filter(
        user=user,
        date=yesterday,
        status='Present'
    ).exists()
    
    attendance_trend = 0
    if yesterday_present:
        if today_attendance and today_attendance.status == 'Present':
            attendance_trend = 0
        else:
            attendance_trend = -100
    elif today_attendance and today_attendance.status == 'Present':
        attendance_trend = 100

    # Get total leave count for the user
    total_leave = LeaveRequest.objects.filter(
        user=user
    ).count()

    # Calculate leave trend
    last_month = today - timedelta(days=30)
    current_month_leave = LeaveRequest.objects.filter(
        user=user,
        created_at__gte=today - timedelta(days=30)
    ).count()
    previous_month_leave = LeaveRequest.objects.filter(
        user=user,
        created_at__lt=today - timedelta(days=30),
        created_at__gte=today - timedelta(days=60)
    ).count()

    leave_trend = 0
    if previous_month_leave > 0:
        leave_trend = ((current_month_leave - previous_month_leave) / previous_month_leave) * 100
    elif current_month_leave > 0:
        leave_trend = 100

    # Get time in/out records for today
    time_records = Attendance.objects.filter(
        user=user,
        date=today
    ).values_list('time_in', 'time_out').first()

    time_in = time_records[0] if time_records and time_records[0] else None
    time_out = time_records[1] if time_records and time_records[1] else None

    total_hours = 0
    if time_in and time_out:
        time_diff = time_out - time_in
        total_hours = time_diff.total_seconds() / 3600

    # Get weekly attendance data for charts
    weekly_data = []
    weekly_labels = []
    weekly_present = []
    weekly_absent = []
    
    for i in range(7):
        date = today - timedelta(days=i)
        attendance = Attendance.objects.filter(
            user=user,
            date=date
        ).first()
        
        weekly_labels.append(date.strftime('%a, %b %d'))  # Format: Mon, Jan 01
        if attendance:
            weekly_present.append(1 if attendance.status == 'Present' else 0)
            weekly_absent.append(1 if attendance.status == 'Absent' else 0)
        else:
            weekly_present.append(0)
            weekly_absent.append(0)
    
    # Reverse the lists to show oldest to newest
    weekly_labels.reverse()
    weekly_present.reverse()
    weekly_absent.reverse()

    # Get monthly leave data for charts
    monthly_leave_data = []
    monthly_labels = []
    
    for i in range(6):  # Last 6 months
        month_start = today.replace(day=1) - timedelta(days=30*i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        leave_count = LeaveRequest.objects.filter(
            user=user,
            start_date__gte=month_start,
            start_date__lte=month_end
        ).count()
        
        monthly_labels.append(month_start.strftime('%b'))  # Month name
        monthly_leave_data.append(leave_count)
    
    # Reverse the lists to show oldest to newest
    monthly_labels.reverse()
    monthly_leave_data.reverse()

    context = {
        'total_present': total_present,
        'attendance_trend': attendance_trend,
        'total_leave': total_leave,
        'leave_trend': leave_trend,
        'time_in': time_in.strftime('%I:%M %p') if time_in else 'Not recorded',
        'time_out': time_out.strftime('%I:%M %p') if time_out else 'Not recorded',
        'total_hours': round(total_hours, 2) if total_hours > 0 else 0,
        'weekly_labels': weekly_labels,
        'weekly_present': weekly_present,
        'weekly_absent': weekly_absent,
        'monthly_labels': monthly_labels,
        'monthly_leave_data': monthly_leave_data
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

def update_profile(request):
    if request.method == 'POST':
        user = request.user
        
        # Update user information
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        
        # Update additional fields if they exist in your User model
        if hasattr(user, 'birthdate'):
            birthdate = request.POST.get('birthdate')
            if birthdate:
                user.birthdate = birthdate
                
        if hasattr(user, 'contact_number'):
            contact_number = request.POST.get('contact_number')
            if contact_number:
                user.contact_number = contact_number
        
        try:
            user.save()
            messages.success(request, 'Profile updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
            
    return redirect('dashboard:employee_profile')

def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Verify current password
        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('dashboard:employee_profile')

        # Check if new passwords match
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('dashboard:employee_profile')

        # Set new password
        user.set_password(new_password)
        user.save()

        # Update session to prevent logout
        update_session_auth_hash(request, user)

        messages.success(request, 'Password changed successfully.')
        return redirect('dashboard:employee_profile')

    return redirect('dashboard:employee_profile')

@api_view(['GET'])
def get_chart_data(request):
    serializer = ChartDataSerializer(instance={})
    return Response(serializer.data)
