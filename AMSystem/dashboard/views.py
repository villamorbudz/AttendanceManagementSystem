from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, LeaveRequest, LeaveBalance
from .forms import LeaveRequestForm
from django.http import HttpResponse

# Consolidated imports for clarity

# Employee Leave Request Views
@login_required
def request_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            messages.success(request, "Your leave request has been submitted.")
            return redirect('leave_status')
    else:
        form = LeaveRequestForm()

    return render(request, 'leave/request_leave.html', {'form': form})

@login_required
def leave_status(request):
    leave_requests = LeaveRequest.objects.filter(employee=request.user)
    return render(request, 'leave/leave_status.html', {'leave_requests': leave_requests})

@login_required
def leave_balance(request):
    # Handle case where the LeaveBalance might not exist for the user
    balance = get_object_or_404(LeaveBalance, employee=request.user)
    return render(request, 'leave/leave_balance.html', {'balance': balance})

# Employee Profile Views
@login_required
def employee_profile(request):
    if request.method == 'POST':
        # Retrieve the updated name and profile image from the form
        name = request.POST.get('name')
        profile_image = request.FILES.get('profile_image')

        # Update user name
        request.user.first_name = name
        request.user.save()

        # Update profile image in the Profile model
        profile, created = Profile.objects.get_or_create(user=request.user)
        if profile_image:
            profile.profile_image = profile_image
        profile.save()

        # Show success message and redirect back to the profile page
        messages.success(request, 'Profile updated successfully!')
        return redirect('employee_profile')  # Ensure 'employee_profile' is in your urls.py

    # Render the profile template
    return render(request, 'dashboard/employee_profile.html')  # Use the correct path here

# Admin Dashboard Views
def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')

def admin_employee_status(request):
    return render(request, 'dashboard/admin_employee_status.html')

# Employee Dashboard Views
def employee_dashboard(request):
    return render(request, 'dashboard/employee_dashboard.html')

def employee_leave_request_dashboard(request):
    return render(request, 'dashboard/employee_leave_request_dashboard.html')

# Handle leave request submission (if needed as an additional view)
def submit_leave_request(request):
    if request.method == "POST":
        # Process leave request logic here
        return HttpResponse("Leave request submitted successfully!")
    return HttpResponse("Invalid request method.")

def admin_leave_management(request):
    return render(request, 'dashboard/admin_leave_management.html')