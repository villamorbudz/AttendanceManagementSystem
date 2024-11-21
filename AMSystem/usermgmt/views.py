from django.shortcuts import render, redirect
from django.contrib import messages
<<<<<<< HEAD
from .forms import UserRegistrationForm
=======
from .forms import UserRegistrationForm, UserProfileForm
from .models import Role, Department
>>>>>>> eadashboard
from django.contrib.auth.decorators import login_required
from userauth.views import redirect_to_dashboard

@login_required
def register(request):
<<<<<<< HEAD
    # Check if the logged-in user has the "Employee" role
    if request.user.department.role.first().name == 'Employee':
        return redirect('employee_dashboard')
=======
    # Only staff and superusers can register new users
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('access_denied')  # Redirect to a custom error page
>>>>>>> eadashboard

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            default_password = '123456'  # To implement default password format: lastnameAMS123456
            user.set_password(default_password)
            user.save()

            messages.success(request, f'Registration successful for {user.first_name} {user.last_name}! '
<<<<<<< HEAD
                                    f'User ID is: {user.user_id}. '
                                    'Ensure the employee password is changed after the first login.')
=======
                                      f'User ID is: {user.user_id}. '
                                      'Ensure the employee password is changed after the first login.')
            # Redirect based on user role
            if user.role.name == 'Employee':
                return redirect('employee_dashboard')  # Redirect to employee dashboard
            else:
                return redirect('success_page')  # Redirect to success page for other roles
>>>>>>> eadashboard
    else:
        form = UserRegistrationForm()

    return render(request, 'usermgmt/registration.html', {'form': form})
<<<<<<< HEAD
=======


@login_required
def employee_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if not user.first_name:
                messages.error(request, "First name is required.")
            else:
                user.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'employee_profile.html', {'form': form})


def success_page(request):
    return render(request, 'usermgmt/success.html')
>>>>>>> eadashboard
