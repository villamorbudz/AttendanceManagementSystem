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
                # Store the actual password in session
                request.session['password_text'] = password
                
                if next_url:
                    return redirect(next_url)
                return redirect_to_dashboard(request)
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = UserAuthenticationForm()

    return render(request, 'userauth/login.html', {'form': form})

def logout_view(request):
    
    # Clear the password from session before logout
    if 'password_text' in request.session:
        del request.session['password_text']
    request.session.flush()
    logout(request)
    return redirect('userauth:login')

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
            elif role_name == 'Manager':
                return redirect('dashboard:manager_dashboard')
            elif role_name == 'Administrator':
                return redirect('admin:index')
        else:
            return redirect('login')
    else:
        return redirect('login')