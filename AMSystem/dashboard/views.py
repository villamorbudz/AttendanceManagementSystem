# dashboard/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from django.contrib.auth.models import User
from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from django.contrib.auth import logout
# from django.shortcuts import redirect

# def login_view(request):
#     return render(request, 'userauth/login.html')

# def logout_view(request):
#     logout(request)
#     return redirect('login')

# def admin_dashboard(request):
#     return render(request, 'dashboard/admin_dashboard.html')

# Other views
def submit_leave_request(request):
    if request.method == "POST":
        # Process leave request logic
        return HttpResponse("Leave request submitted successfully!")
    return HttpResponse("Invalid request method.")


def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')

def admin_employee_status(request):
    return render(request, 'dashboard/admin_employee_status.html')

def employee_dashboard(request):
    return render(request, 'dashboard/employee_dashboard.html')

def employee_Leave_Request_dashboard(request):
    return render(request, 'dashboard/employee_Leave_Request_dashboard.html')

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
        return redirect('employee_profile')  # Make sure 'profile' is defined in your urls.py

    # Render the profile template
    return render(request, 'dashboard/employee_profile.html')  # Use the correct path here

@login_required
def profile(request):
    return render(request, 'dashboard/employee_profile.html')