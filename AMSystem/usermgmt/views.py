from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import Role, Department  
from django.contrib.auth.decorators import login_required

@login_required  # Ensure the user is logged in
def register(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('access_denied')  # Redirect to a custom error page

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            default_password = '123456'
            user.set_password(default_password)

            # Assign role based on department logic
            department = form.cleaned_data.get('department')
            if department and department.name == 'Dev Team':
                user.role = Role.objects.get(name='Administrator')
            else:
                user.role = Role.objects.get(name='Employee')
            user.save()

            messages.success(request, f'Registration successful for {user.first_name} {user.last_name}! '
                                        f'User ID is: {user.user_id}. '
                                        'Ensure the employee password is changed after the first login.')
            if user.role.name == 'Employee':
                return redirect('employee_dashboard')  # Redirect to employee dashboard for employees
            else:
                return redirect('success_page')  # Redirect to success page for other roles
    else:
        form = UserRegistrationForm()

    return render(request, 'usermgmt/registration.html', {'form': form})

def success_page(request):
    return render(request, 'usermgmt/success.html')