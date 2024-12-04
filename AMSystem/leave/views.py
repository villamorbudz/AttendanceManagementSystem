from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from .models import LeaveRequest, LeaveType
from .forms import LeaveRequestForm
from django.contrib import messages
from userauth.views import redirect_to_dashboard

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
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.status = 'Pending'
            leave.save()
            messages.success(request, 'Leave request submitted successfully')
        else:
            messages.error(request, 'Leave request unsuccessful. Please correct the errors below.')
    else:
        form = LeaveRequestForm()
    
    context = {
        'form': form,
        'leave_types': LeaveType.objects.all(),
        'user': request.user
    }
    return render(request, 'leave/leave_request.html', context)