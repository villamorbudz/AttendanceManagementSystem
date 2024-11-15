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

    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            
            user = authenticate(request, user_id=user_id, password=password)
            if user:
                login(request, user)
                return redirect_to_dashboard(request)
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = UserAuthenticationForm()

    return render(request, 'userauth/login.html', {'form': form})

def landing(request):
    return render(request, 'userauth/landingPage.html')

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
                return redirect('employee_dashboard')
            elif role_name == 'Administrator':
                return redirect('home')
            elif role_name == 'System Administrator':
                return redirect('../admin/dashboard')
        else:
            return redirect('login')
    else:
        return redirect('login')
