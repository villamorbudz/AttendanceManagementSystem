# userauth/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import UserAuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)

        if form.is_valid():
            employee_id = form.cleaned_data['employee_id']
            password = form.cleaned_data['password']

            # This will use the EmployeeBackend you defined
            user = authenticate(request, username=employee_id, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid employee ID or password.')
    else:
        form = UserAuthenticationForm()

    return render(request, 'userauth/login.html', {'form': form})

def index(request):
    return render(request, 'userauth/index.html')

def landing(request):
    return render(request, 'userauth/landingPage.html')
