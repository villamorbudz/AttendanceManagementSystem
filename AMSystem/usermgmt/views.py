from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            employee = form.save(commit=False)
            default_password = '123456'
            employee.set_password(default_password)  # Set the default password
            employee.save()

            messages.success(request, f'Registration successful for {employee.first_name} {employee.last_name}! '
                                      f'Employee ID is {employee.employee_id}.'
                                      'Ensure the employee password is changed after the first login.')
    else:
        form = UserRegistrationForm()

    return render(request, 'usermgmt/registration.html', {'form': form})
