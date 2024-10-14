from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.set_password(form.cleaned_data['password'])
            employee.save()
            employee.username = str(employee.employee_id)
            employee.save()
            messages.success(request, f'Registration successful for {employee.first_name} {employee.last_name}! Employee ID is {employee.employee_id}.')
            return redirect('register') 
    else:
        form = UserRegistrationForm()
    return render(request, 'usermgmt/registration.html', {'form': form})
