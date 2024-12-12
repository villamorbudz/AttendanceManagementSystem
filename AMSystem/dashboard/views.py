"""
Dashboard views for the Attendance Management System.
This module contains views for both manager and employee dashboards.
"""

# Django imports
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.db import IntegrityError

# Rest framework imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Model imports
from attendance.models import Attendance
from leave.models import LeaveRequest, LeaveType
from management.models import Department, Role, User
from management import views as management_views
from .serializers import ChartDataSerializer

# Python standard library
import json
import logging
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

# Common views
@login_required
def dashboard_home(request):
    """Home view for the dashboard."""
    return render(request, 'dashboard/home.html')


@login_required
def employee_profile(request):
    """Employee profile view showing user information and password."""
    password_text = request.session.get('password_text', '')
    context = {
        'user': request.user,
        'password_text': password_text
    }
    return render(request, 'dashboard/employee/employee_profile.html', context)


@login_required
def employee_attendance(request):
    """View for employee attendance history and records."""
    time_period = request.GET.get('time_period', 'all_time')
    
    # Get the current date
    current_date = timezone.now().date()
    
    # Define the date range based on the selected time period
    if time_period == 'today':
        start_date = current_date
    elif time_period == 'week':
        start_date = current_date - timedelta(days=7)
    elif time_period == 'month':
        start_date = current_date - timedelta(days=30)
    else:  # all_time
        start_date = None
    
    # Query attendance records
    attendance_query = Attendance.objects.filter(user=request.user)
    if start_date:
        attendance_query = attendance_query.filter(date__gte=start_date)
    
    attendance_records = attendance_query.order_by('-date')
    
    context = {
        'attendance_records': attendance_records,
        'selected_period': time_period
    }
    return render(request, 'dashboard/employee/employee_manage_attendance.html', context)

@login_required
def employee_leave(request):
    """View for employee leave requests and history."""
    leave_requests = LeaveRequest.objects.filter(user=request.user).order_by('-created_at')
    leave_types = LeaveType.objects.filter(is_active=True)
    context = {
        'leave_requests': leave_requests,
        'leave_types': leave_types
    }
    return render(request, 'dashboard/employee/employee_leave.html', context)

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

@login_required
def manager_profile(request):
    """Manager profile view."""
    password_text = request.session.get('password_text', '')
    context = {
        'user': request.user,
        'password_text': password_text
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

@login_required
def manager_attendance(request):
    """View for managing department attendance."""
    attendance_records = Attendance.objects.filter(
        user__department=request.user.department
    ).select_related('user').order_by('-date')
    context = {'attendance_records': attendance_records}
    return render(request, 'dashboard/manager/manager_attendance.html', context)

@login_required
def manager_user_management(request):
    """View for managing department employees."""
    users = User.objects.all()
    departments = Department.objects.all()
    roles = Role.objects.all()
    context = {'users': users, 'departments': departments, 'roles': roles}
    return render(request, 'dashboard/manager/manager_user_management.html', context)

    
@login_required
def manager_departments(request):
    """View for department management."""
    # Get all departments from the database with ordering, including inactive ones
    departments_list = Department.objects.all().order_by('-is_active', 'name')
    roles = Role.objects.all()
    
    # Add employee count and role info for each department
    for dept in departments_list:
        dept.employees_count = User.objects.filter(department=dept).count()
        dept.role_name = dept.role.first().name if dept.role.exists() else "No Role"
    
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
        'roles': roles,
        'total_departments': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': int(page)
    })

@login_required
def manager_roles(request):
    """View for managing roles."""
    # Get all roles
    roles = Role.objects.all().order_by('name')
    users = User.objects.all()
    
    # Get user count for each role by counting users in departments with that role
    for role in roles:
        role.user_count = User.objects.filter(department__role=role).count()
        
    context = {
        'roles': roles,
    }
    return render(request, 'dashboard/manager/manager_manage_roles.html', context)

@login_required
def manager_leave_types(request):
    """View for managing leave types."""
    leave_types = LeaveType.objects.all().order_by('-is_active', 'name')
    context = {
        'leave_types': leave_types,
    }
    return render(request, 'dashboard/manager/manager_manage_leave_type.html', context)

@login_required
def manager_leave(request):
    """View for managing leave requests."""
    leave_requests = LeaveRequest.objects.filter(
        user__department=request.user.department
    ).select_related('user', 'leave_type').order_by('-created_at')
    context = {'leave_requests': leave_requests}
    return render(request, 'dashboard/manager/manager_leave.html', context)

@login_required
def manager_leave_requests(request):
    # Get all leave requests with related data
    leave_requests_list = LeaveRequest.objects.select_related(
        'user', 'user__department', 'leave_type'
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
    
    # Annotate additional fields for display
    leave_requests_list = leave_requests_list.annotate(
        department_name=F('user__department__name'),
        user_full_name=Concat('user__first_name', Value(' '), 'user__last_name'),
        leave_type_name=F('leave_type__name')
    )
    
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
    
    # Get all active departments for the filter
    departments = Department.objects.filter(is_active=True)
    
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
            leave_request.status = 'Approved'
        elif action == 'reject':
            leave_request.status = 'Rejected'
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
def employee_dashboard(request):
    return render(request, 'dashboard/employee/employee_dashboard.html')

@login_required
def department_management(request):
    departments = Department.objects.all()
    context = {
        'departments': departments,
        'active_page': 'department_management'
    }
    return render(request, 'dashboard/manager/manager_department_management.html', context)

@login_required
def add_department(request):
    if request.method == 'POST':
        try:
            return management_views.department_create(request)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

@login_required
def update_department(request, department_id):
    if request.method == 'POST':
        try:
            return management_views.department_update(request, department_id)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

@login_required
def delete_department(request, department_id):
    """Delete a department."""
    if request.method == 'POST':
        try:
            return management_views.department_delete(request, department_id)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

@login_required
def restore_department(request, department_id):
    """Restore a soft-deleted department."""
    if request.method == 'POST':
        try:
            return management_views.department_restore(request, department_id)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


@login_required
def delete_user(request):
    """Handle user deletion (soft delete)."""
    if request.method != 'DELETE':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'message': 'User ID is required'}, status=400)
            
        response = management_views.user_delete(request, user_id)
        return response
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
def restore_user(request):
    """Handle user restoration."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'message': 'User ID is required'}, status=400)
            
        try:
            user = User.objects.get(user_id=user_id)
            # Check if user's department has System Administrator role
            is_sys_admin = user.department.role.filter(name='System Administrator').exists()
            
            if is_sys_admin and not user.is_active:
                return JsonResponse({
                    'success': False, 
                    'message': 'System Administrator accounts cannot be modified.'
                }, status=403)
            
            user.is_active = True
            user.save()
            return JsonResponse({
                'success': True,
                'message': 'User restored successfully'
            })
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'User not found'
            }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
def get_user_info(request, user_id):
    """Get user information for the edit form."""
    try:
        user = User.objects.get(user_id=user_id)
        birthdate = user.birthdate.strftime('%Y-%m-%d') if user.birthdate else ''
        data = {
            'success': True,
            'user': {
                'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'birthdate': birthdate,
                'contact_number': user.contact_number or '',
                'department_id': user.department.id if user.department else '',
            }
        }
        return JsonResponse(data)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found'}, status=404)
    except Exception as e:
        logger.error(f"Error fetching user info: {str(e)}")
        return JsonResponse({'success': False, 'message': 'An error occurred while fetching user information'}, status=500)

# API views
@api_view(['GET'])
def get_chart_data(request):
    """API endpoint for chart data."""
    serializer = ChartDataSerializer(instance={})
    return Response(serializer.data)

@api_view(['GET'])
@login_required
def get_user_data(request, user_id):
    """API endpoint to get user data for edit form."""
    try:
        user = User.objects.get(id=user_id)
        if user.department.name == 'Development Team':
            return Response({'error': 'Cannot edit Development Team members'}, status=status.HTTP_403_FORBIDDEN)
        
        data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'contact_number': user.contact_number,
            'department': user.department.id if user.department else None,
            'user_id': user.user_id,
        }
        return Response(data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@login_required
def update_user(request):
    """Handle user updates."""
    if request.method not in ['PUT', 'POST']:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
    
    try:
        if request.method == 'POST':
            data = request.POST.dict()
        else:  # PUT
            data = json.loads(request.body)
            
        user_id = data.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'message': 'User ID is required'}, status=400)
            
        response = management_views.user_update(request, user_id)
        return response
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
def update_profile(request):
    """Handle employee profile updates."""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.contact_number = request.POST.get('contact_number', user.contact_number)
        user.save()
        messages.success(request, 'Profile updated successfully.')
    return redirect('dashboard:employee_profile')

@login_required
def change_password(request):
    """Handle employee password changes."""
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user
        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('dashboard:employee_profile')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('dashboard:employee_profile')

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        request.session['password_text'] = new_password
        messages.success(request, 'Password changed successfully.')
    return redirect('dashboard:employee_profile')

@login_required
def leave_type_add(request):
    """Add a new leave type."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    try:
        data = json.loads(request.body)
        name = data.get('name')
        
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
            
        # Create new leave type
        leave_type = LeaveType.objects.create(name=name)
        
        return JsonResponse({
            'success': True,
            'message': 'Leave type created successfully',
            'leave_type': {
                'id': leave_type.id,
                'name': leave_type.name,
                'is_active': leave_type.is_active
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except IntegrityError:
        return JsonResponse({'error': 'A leave type with this name already exists'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def leave_type_edit(request, leave_type_id):
    """Edit a leave type."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    try:
        leave_type = LeaveType.objects.get(id=leave_type_id)
        data = json.loads(request.body)
        name = data.get('name')
        
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
            
        # Update leave type
        leave_type.name = name
        leave_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Leave type updated successfully',
            'leave_type': {
                'id': leave_type.id,
                'name': leave_type.name,
                'is_active': leave_type.is_active
            }
        })
    except LeaveType.DoesNotExist:
        return JsonResponse({'error': 'Leave type not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except IntegrityError:
        return JsonResponse({'error': 'A leave type with this name already exists'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def leave_type_delete(request, leave_type_id):
    """Soft delete a leave type."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    try:
        leave_type = LeaveType.objects.get(id=leave_type_id)
        
        # Soft delete by setting is_active to False
        leave_type.is_active = False
        leave_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Leave type deactivated successfully'
        })
    except LeaveType.DoesNotExist:
        return JsonResponse({'error': 'Leave type not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def leave_type_restore(request, leave_type_id):
    """Restore a soft-deleted leave type."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    try:
        leave_type = LeaveType.objects.get(id=leave_type_id)
        
        # Restore by setting is_active to True
        leave_type.is_active = True
        leave_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Leave type restored successfully'
        })
    except LeaveType.DoesNotExist:
        return JsonResponse({'error': 'Leave type not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)