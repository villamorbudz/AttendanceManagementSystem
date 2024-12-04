# userauth/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserAuthenticationForm
from django.contrib.auth import get_user_model

def login_view(request):
    if request.user.is_authenticated:
        logout(request)

    # Get next URL from either GET or POST parameters
    next_url = request.POST.get('next') or request.GET.get('next')

    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            
            user = authenticate(request, user_id=user_id, password=password)
            if user:
                login(request, user)
                
                if next_url:
                    return redirect(next_url)
                return redirect_to_dashboard(request)
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = UserAuthenticationForm()

    return render(request, 'userauth/login.html', {'form': form})

def index(request):
    return render(request, 'userauth/index.html')

def clear_messages_view(request):
    storage = messages.get_messages(request)
    storage.used = True

def redirect_to_dashboard(request):
    if request.user.is_authenticated:
        department = request.user.department
        role = department.role.first()

        if role:
            role_name = role.name

            if role_name == 'Employee':
                return redirect('dashboard:employee_dashboard')
            elif role_name == 'Administrator':
                return redirect('dashboard:manager_dashboard')
            elif role_name == 'System Administrator':
                return redirect('admin:index')
        else:
            return redirect('login')
    else:
        return redirect('login')