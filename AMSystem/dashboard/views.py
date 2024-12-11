"""
Dashboard views for the Attendance Management System.
This module contains views for both manager and employee dashboards.
"""

# Django imports
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth import get_user_model

# Rest framework imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Model imports
from attendance.models import Attendance
from leave.models import LeaveRequest
from management.models import Department, Role, User
from management import views as management_views
from .serializers import ChartDataSerializer

# Python standard library
import json
import logging
from datetime import timedelta

# Get the User model
User = get_user_model()

# Initialize logger
logger = logging.getLogger(__name__)

# Common views
@login_required
def dashboard_home(request):
    """Home view for the dashboard."""
    return render(request, 'dashboard/home.html')

# Employee views
@login_required
def employee_dashboard(request):
    """Employee dashboard view showing attendance summary."""
    context = {
        'attendance_summary': {
            'present': 22,
            'absent': 3,
            'late': 5
        }
    }
    return render(request, 'dashboard/employee/employee_dashboard.html', context)

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
    return render(request, 'dashboard/employee/employee_attendance.html', context)

@login_required
def employee_leave(request):
    """View for employee leave requests and history."""
    leave_requests = LeaveRequest.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'leave_requests': leave_requests
    }
    return render(request, 'dashboard/employee/employee_leave.html', context)

# Manager views
@login_required
def manager_dashboard(request):
    """Manager dashboard view showing department statistics."""
    attendance_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    attendance_data = [45, 42, 47, 44, 45]
    leave_stats = [10, 5, 2]  # Approved, Pending, Rejected

    context = {
        'attendance_labels': json.dumps(attendance_labels),
        'attendance_data': json.dumps(attendance_data),
        'leave_stats': json.dumps(leave_stats),
    }
    return render(request, 'dashboard/manager/manager_dashboard.html', context)

@login_required
def manager_profile(request):
    """Manager profile view."""
    context = {
        'user': request.user
    }
    return render(request, 'dashboard/manager/manager_profile.html', context)

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
    users = User.objects.all()
    departments = Department.objects.all()
    roles = Role.objects.all()
    
    # Add employee count and role info for each department
    for dept in departments:
        dept.employees_count = User.objects.filter(department=dept).count()
        dept.role_name = dept.role.first().name if dept.role.exists() else "No Role"
    
    context = {'users': users, 'departments': departments, 'roles': roles}
    return render(request, 'dashboard/manager/manager_manage_departments.html', context)

@login_required
def manager_leave_types(request):
    """View for managing leave types."""
    leave_types = LeaveRequest.objects.filter(
        user__department=request.user.department
    ).values('leave_type__name').annotate(count=Count('id'))
    return render(request, 'dashboard/manager/manager_manage_leave_type.html', 
                {'leave_types': leave_types})

@login_required
def manager_leave(request):
    """View for managing leave requests."""
    leave_requests = LeaveRequest.objects.filter(
        user__department=request.user.department
    ).select_related('user', 'leave_type').order_by('-created_at')
    context = {'leave_requests': leave_requests}
    return render(request, 'dashboard/manager/manager_leave.html', context)

@login_required
def manager_roles(request):
    """View for role management."""
    roles = Role.objects.all()
    # Add user count for each role through department relationship
    for role in roles:
        # Get all departments that have this role
        departments = role.departments.all()
        # Count users in those departments
        role.users_count = User.objects.filter(department__in=departments).count()
    context = {
        'roles': roles,
    }
    return render(request, 'dashboard/manager/manager_manage_roles.html', context)

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
def delete_department(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            department_id = data.get('id')
            return management_views.department_delete(request, department_id)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
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