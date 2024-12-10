from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from userauth.views import redirect_to_dashboard
from django.contrib.auth.hashers import make_password
import csv
import io
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Department
from django.db import transaction
from datetime import datetime
from attendance.models import Attendance
from leave.models import LeaveRequest, LeaveType
import json

# User CRUD Views
@login_required
def user_list(request):
    users = get_user_model().objects.filter(is_active=True)
    return JsonResponse({'users': list(users.values())})

@login_required
def user_detail(request, user_id):
    try:
        user = get_user_model().objects.get(user_id=user_id, is_active=True)
        return JsonResponse({'user': {
            'id': user.id,
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'contact_number': user.contact_number,
            'birthdate': user.birthdate,
            'department': user.department.name
        }})
    except get_user_model().DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@login_required
def user_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            department = Department.objects.get(id=data['department'])
            user = get_user_model().objects.create(
                user_id=data['user_id'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                contact_number=data['contact_number'],
                birthdate=data['birthdate'],
                department=department
            )
            user.set_password(data.get('password', '123456'))  # Default password if not provided
            user.save()
            return JsonResponse({'message': 'User created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def user_update(request, user_id):
    if request.method == 'PUT':
        try:
            user = get_user_model().objects.get(user_id=user_id, is_active=True)
            data = json.loads(request.body)
            
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
            if 'email' in data:
                user.email = data['email']
            if 'contact_number' in data:
                user.contact_number = data['contact_number']
            if 'birthdate' in data:
                user.birthdate = data['birthdate']
            if 'department' in data:
                department = Department.objects.get(id=data['department'])
                user.department = department
            if 'password' in data:
                user.set_password(data['password'])
            
            user.save()
            return JsonResponse({'message': 'User updated successfully'})
        except get_user_model().DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def user_delete(request, user_id):
    if request.method == 'DELETE':
        try:
            user = get_user_model().objects.get(user_id=user_id, is_active=True)
            user.is_active = False  # Soft delete
            user.save()
            return JsonResponse({'message': 'User deleted successfully'})
        except get_user_model().DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Role CRUD Views
@login_required
def role_list(request):
    roles = get_user_model()._meta.get_field('role').related_model.objects.all()
    return JsonResponse({'roles': list(roles.values())})

@login_required
def role_detail(request, role_id):
    try:
        role = get_user_model()._meta.get_field('role').related_model.objects.get(id=role_id)
        return JsonResponse({'role': {
            'id': role.id,
            'name': role.name,
            'is_staff': role.is_staff,
            'is_superuser': role.is_superuser
        }})
    except get_user_model()._meta.get_field('role').related_model.DoesNotExist:
        return JsonResponse({'error': 'Role not found'}, status=404)

@login_required
def role_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            role = get_user_model()._meta.get_field('role').related_model.objects.create(
                name=data['name'],
                is_staff=data.get('is_staff', False),
                is_superuser=data.get('is_superuser', False)
            )
            return JsonResponse({'message': 'Role created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def role_update(request, role_id):
    if request.method == 'PUT':
        try:
            role = get_user_model()._meta.get_field('role').related_model.objects.get(id=role_id)
            data = json.loads(request.body)
            
            if 'name' in data:
                role.name = data['name']
            if 'is_staff' in data:
                role.is_staff = data['is_staff']
            if 'is_superuser' in data:
                role.is_superuser = data['is_superuser']
            
            role.save()
            return JsonResponse({'message': 'Role updated successfully'})
        except get_user_model()._meta.get_field('role').related_model.DoesNotExist:
            return JsonResponse({'error': 'Role not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def role_delete(request, role_id):
    if request.method == 'DELETE':
        try:
            role = get_user_model()._meta.get_field('role').related_model.objects.get(id=role_id)
            # Check if any departments are using this role
            if role.departments.exists():
                return JsonResponse({'error': 'Cannot delete role as it is associated with departments'}, status=400)
            role.delete()  # Roles don't have is_active field
            return JsonResponse({'message': 'Role deleted successfully'})
        except get_user_model()._meta.get_field('role').related_model.DoesNotExist:
            return JsonResponse({'error': 'Role not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Department CRUD Views
@login_required
def department_list(request):
    departments = Department.objects.all()
    return JsonResponse({'departments': [{
        'id': dept.id,
        'name': dept.name,
        'roles': list(dept.role.values('id', 'name'))
    } for dept in departments]})

@login_required
def department_detail(request, department_id):
    try:
        department = Department.objects.get(id=department_id)
        return JsonResponse({'department': {
            'id': department.id,
            'name': department.name,
            'roles': list(department.role.values('id', 'name'))
        }})
    except Department.DoesNotExist:
        return JsonResponse({'error': 'Department not found'}, status=404)

@login_required
def department_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            department = Department.objects.create(name=data['name'])
            if 'roles' in data:
                roles = get_user_model()._meta.get_field('role').related_model.objects.filter(id__in=data['roles'])
                department.role.set(roles)
            return JsonResponse({'message': 'Department created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def department_update(request, department_id):
    if request.method == 'PUT':
        try:
            department = Department.objects.get(id=department_id)
            data = json.loads(request.body)
            
            if 'name' in data:
                department.name = data['name']
            if 'roles' in data:
                roles = get_user_model()._meta.get_field('role').related_model.objects.filter(id__in=data['roles'])
                department.role.set(roles)
            
            department.save()
            return JsonResponse({'message': 'Department updated successfully'})
        except Department.DoesNotExist:
            return JsonResponse({'error': 'Department not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def department_delete(request, department_id):
    if request.method == 'DELETE':
        try:
            department = Department.objects.get(id=department_id)
            # Check if any users are in this department
            if get_user_model().objects.filter(department=department, is_active=True).exists():
                return JsonResponse({'error': 'Cannot delete department as it has active users'}, status=400)
            department.delete()  # Departments don't have is_active field
            return JsonResponse({'message': 'Department deleted successfully'})
        except Department.DoesNotExist:
            return JsonResponse({'error': 'Department not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# User Registration Views
@login_required
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User registered successfully')
            return redirect('management:success')
        else:
            messages.error(request, 'Registration unsuccessful. Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'management/registration.html', {'form': form})

@login_required
def success_page(request):
    return render(request, 'management/success.html')

# Attendance Management Views
@login_required
def leave_request_list(request):
    if request.user.department.role.first().name != 'Manager':
        leave_requests = LeaveRequest.objects.filter(user=request.user)
    else:
        leave_requests = LeaveRequest.objects.filter(user__department=request.user.department)
    return JsonResponse({'leave_requests': list(leave_requests.values())})

@login_required
def leave_request_detail(request, request_id):
    try:
        leave_request = LeaveRequest.objects.get(id=request_id)
        if request.user.department.role.first().name != 'Manager' and leave_request.user != request.user:
            return JsonResponse({'error': 'Unauthorized access'}, status=403)
        return JsonResponse({
            'leave_request': {
                'id': leave_request.id,
                'user': leave_request.user.get_full_name(),
                'leave_type': leave_request.leave_type.name,
                'start_date': leave_request.start_date,
                'end_date': leave_request.end_date,
                'reason': leave_request.reason,
                'status': leave_request.status
            }
        })
    except LeaveRequest.DoesNotExist:
        return JsonResponse({'error': 'Leave request not found'}, status=404)

@login_required
def leave_request_update(request, request_id):
    if request.method == 'PUT':
        try:
            leave_request = LeaveRequest.objects.get(id=request_id)
            if request.user.department.role.first().name != 'Manager':
                return JsonResponse({'error': 'Unauthorized access'}, status=403)
            
            data = json.loads(request.body)
            if 'status' in data:
                leave_request.status = data['status']
                leave_request.save()
                return JsonResponse({'message': 'Leave request updated successfully'})
            return JsonResponse({'error': 'Status field is required'}, status=400)
        except LeaveRequest.DoesNotExist:
            return JsonResponse({'error': 'Leave request not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# CSV Import Views
@login_required
def bulk_register(request):
    if request.method == 'POST':
        try:
            csv_file = request.FILES.get('csv_file')
            if not csv_file:
                messages.error(request, 'No file was uploaded')
                return redirect('management:bulk_register')
                
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a CSV file')
                return redirect('management:bulk_register')

            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.DictReader(io.StringIO(decoded_file))
            
            with transaction.atomic():
                for row in csv_data:
                    try:
                        department = Department.objects.get(name=row['department'])
                        user = get_user_model().objects.create(
                            user_id=row['user_id'],
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                            email=row['email'],
                            contact_number=row.get('contact_number', ''),
                            birthdate=datetime.strptime(row['birthdate'], '%Y-%m-%d').date(),
                            department=department
                        )
                        user.set_password(row.get('password', '123456'))  # Default password if not provided
                        user.save()
                    except Exception as e:
                        messages.error(request, f'Error processing row for user {row.get("user_id", "unknown")}: {str(e)}')
                        return redirect('management:bulk_register')
                
            messages.success(request, 'Users registered successfully')
            return redirect('management:success')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('management:bulk_register')
    return render(request, 'management/bulk_registration.html')

@login_required
def bulk_attendance(request):
    if request.method == 'POST':
        try:
            csv_file = request.FILES.get('csv_file')
            if not csv_file:
                messages.error(request, 'No file was uploaded')
                return redirect('management:bulk_attendance')
                
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a CSV file')
                return redirect('management:bulk_attendance')

            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.DictReader(io.StringIO(decoded_file))
            
            with transaction.atomic():
                for row in csv_data:
                    try:
                        user = get_user_model().objects.get(user_id=row['user_id'])
                        date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                        time_in = datetime.strptime(row['time_in'], '%H:%M').time() if row['time_in'] else None
                        time_out = datetime.strptime(row['time_out'], '%H:%M').time() if row['time_out'] else None
                        
                        attendance, created = Attendance.objects.update_or_create(
                            user=user,
                            date=date,
                            defaults={
                                'time_in': time_in,
                                'time_out': time_out
                            }
                        )
                    except (get_user_model().DoesNotExist, ValueError, KeyError) as e:
                        messages.error(request, f'Error processing row for user {row.get("user_id", "unknown")}: {str(e)}')
                        return redirect('management:bulk_attendance')
                
            messages.success(request, 'Attendance records uploaded successfully')
            return redirect('management:success')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('management:bulk_attendance')
    return render(request, 'management/bulk_attendance.html')

@login_required
def bulk_leave_requests(request):
    if request.method == 'POST':
        try:
            csv_file = request.FILES.get('csv_file')
            if not csv_file:
                messages.error(request, 'No file was uploaded')
                return redirect('management:bulk_leave_requests')
                
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a CSV file')
                return redirect('management:bulk_leave_requests')

            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.DictReader(io.StringIO(decoded_file))
            
            with transaction.atomic():
                for row in csv_data:
                    try:
                        user = get_user_model().objects.get(user_id=row['user_id'])
                        leave_type = LeaveType.objects.get(name=row['leave_type'])
                        start_date = datetime.strptime(row['start_date'], '%Y-%m-%d').date()
                        end_date = datetime.strptime(row['end_date'], '%Y-%m-%d').date()
                        
                        leave_request = LeaveRequest.objects.create(
                            user=user,
                            leave_type=leave_type,
                            start_date=start_date,
                            end_date=end_date,
                            reason=row.get('reason', ''),
                            status='Pending'
                        )
                    except Exception as e:
                        messages.error(request, f'Error processing row for user {row.get("user_id", "unknown")}: {str(e)}')
                        return redirect('management:bulk_leave_requests')
                
            messages.success(request, 'Leave requests created successfully')
            return redirect('management:success')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('management:bulk_leave_requests')
    return render(request, 'management/bulk_leave_requests.html')
