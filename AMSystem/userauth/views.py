# userauth/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from usermgmt.models import User
from usermgmt.views import register  # Import the register view from usermgmt
from .forms import UserAuthenticationForm



# def login_view(request):
#     if request.method == 'POST':
#         form = UserAuthenticationForm(request.POST)
#         if form.is_valid():
#             user_id = form.cleaned_data['user_id']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=user_id, password=password)
#             if user is not None:
#                 auth_login(request, user)
#                 messages.success(request, 'Successfully logged in!')
#                 if user.is_superuser:
#                     return redirect('admin_dashboard')  # Ensure this is correct
#                 else:
#                     return redirect('employee_dashboard')  # For non-admin users
#             else:
#                 messages.error(request, 'Invalid credentials. Please try again.')
#     else:
#         form = UserAuthenticationForm()
    
#     return render(request, 'userauth/login.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)

        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']

            # Check if the user exists in usermgmt.User
            if User.objects.filter(user_id=user_id).exists():
                user = authenticate(request, username=user_id, password=password)
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, 'Successfully logged in!')
                    if user.is_superuser:
                        return redirect('/admin/')  # Redirect to Django admin for superusers
                    else:
                        return redirect('employee_dashboard')  # Redirect to employee dashboard for regular users
                else:
                    messages.error(request, 'Invalid credentials. Please try again.')
            else:
                messages.error(request, 'User does not exist.')

    else:
        form = UserAuthenticationForm()

    return render(request, 'userauth/login.html', {'form': form})

def index(request):
    return render(request, 'userauth/index.html')

def landing(request):
    return render(request, 'userauth/landingPage.html')

def access_denied(request):
    return render(request, 'userauth/access_denied.html')

def employee_dashboard(request):
    return render(request, 'dashboard/employee_dashboard.html')
