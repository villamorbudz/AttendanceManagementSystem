from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django import forms
from .models import LeaveRequest, LeaveType
from .forms import LeaveRequestForm
from django.contrib import messages
from userauth.views import redirect_to_dashboard
from django.utils import timezone
import json

# Create your views here.

class LeaveRequestForm(forms.ModelForm):
    leave_type = forms.ModelChoiceField(queryset=LeaveType.objects.all(), required=True)

    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']

@login_required
def leave_request(request):
    if request.user.department.role.first().name != 'Employee':
        return redirect_to_dashboard(request)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            leave_type = LeaveType.objects.get(id=data.get('leave_type'))
            
            leave = LeaveRequest(
                user=request.user,
                leave_type=leave_type,
                start_date=data.get('start_date'),
                end_date=data.get('end_date'),
                reason=data.get('reason'),
                status='Pending'
            )
            leave.save()
            return JsonResponse({
                'success': True,
                'message': 'Leave request submitted successfully'
            })
        except LeaveType.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Invalid leave type selected'
            }, status=400)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid data format'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    context = {
        'leave_types': LeaveType.objects.filter(is_active=True)
    }
    return render(request, 'leave/leave_request.html', context)

@login_required
def leave_request_update(request, request_id):
    if request.method == 'PUT':
        try:
            leave_request = LeaveRequest.objects.get(id=request_id)
            if request.user.department.role.first().name != 'Manager':
                return JsonResponse({'error': 'Unauthorized access'}, status=403)
            
            data = json.loads(request.body)
            if 'status' not in data:
                return JsonResponse({'error': 'Status field is required'}, status=400)
            
            leave_request.status = data['status']
            leave_request.remark = data.get('remark', '')
            leave_request.processed_by = request.user
            leave_request.processed_at = timezone.now()
            leave_request.save()
            
            return JsonResponse({
                'message': f'Leave request {leave_request.status.lower()} successfully'
            })
            
        except LeaveRequest.DoesNotExist:
            return JsonResponse({'error': 'Leave request not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def process_leave_request(request, request_id, action):
    """
    Process (approve/reject) a leave request with optional remarks.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    if  request.user.department.role.first().name == 'Employee':
        return JsonResponse({'error': 'Unauthorized access'}, status=403)
        
    try:
        leave_request = LeaveRequest.objects.get(id=request_id)
        
        # Validate action
        if action not in ['approve', 'reject']:
            return JsonResponse({'error': 'Invalid action'}, status=400)
            
        # Get data from request body
        try:
            data = json.loads(request.body)
            remark = data.get('remark', '')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
            
        # Update leave request
        leave_request.status = 'Approved' if action == 'approve' else 'Rejected'
        leave_request.remark = remark
        leave_request.processed_by = request.user
        leave_request.processed_at = timezone.now()
        leave_request.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Leave request has been {leave_request.status.lower()} successfully'
        })
        
    except LeaveRequest.DoesNotExist:
        return JsonResponse({'error': 'Leave request not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)