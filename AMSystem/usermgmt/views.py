from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from userauth.views import redirect_to_dashboard

@login_required
def register(request):
    try:
        if request.user.department.role.first().name == 'Employee':
            return redirect('dasbhboard:employee_dashboard')
    except AttributeError:
        return redirect('userauth:login')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            default_password = '123456'  # To implement default password format: lastnameAMS123456
            user.set_password(make_password(default_password))
            user.save()

            messages.success(request, f'Registration successful for {user.first_name} {user.last_name}! '
                                    f'User ID is: {user.user_id}. '
                                    'Ensure the employee password is changed after the first login.')
    else:
        form = UserRegistrationForm()

    return render(request, 'usermgmt/registration.html', {'form': form})

def success_page(request):
    return render(request, 'usermgmt/success.html')
