from django.shortcuts import render
import json

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
            'get_full_name': 'John Manager',
            'email': 'john.manager@example.com',
            'role': 'Department Manager'
        }
    }
    return render(request, 'dashboard/manager/manager_profile.html', context)

def manager_user_management(request):
    # Sample user data
    users = [
        {
            'get_full_name': 'John Doe',
            'email': 'john.doe@example.com',
            'role': 'Employee',
            'department': 'IT',
            'status': 'Active'
        },
        {
            'get_full_name': 'Jane Smith',
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
        'get_full_name': 'John Doe',
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

def employee_attendance(request):
    return render(request, 'dashboard/employee/employee_manage_attendance.html')

def employee_leave(request):
    """
    View for employee leave management.
    """
    context = {
        'user': request.user,
        'leaves': [  # Sample leave data
            {
                'type': 'Annual Leave',
                'start_date': '2024-01-15',
                'end_date': '2024-01-20',
                'status': 'Pending'
            },
            {
                'type': 'Sick Leave',
                'start_date': '2024-02-01',
                'end_date': '2024-02-02',
                'status': 'Approved'
            }
        ]
    }
    return render(request, 'dashboard/employee/employee_leave.html', context)

def logout_view(request):
    from django.contrib.auth import logout
    from django.shortcuts import redirect
    
    logout(request)
    return redirect('login')  # Redirect to your login page URL name
