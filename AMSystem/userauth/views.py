# userauth/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from usermgmt.models import User
from .forms import UserAuthenticationForm

def login_view(request):
    logout(request) # to optimize

    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            
            # Check if the user exists in the User model
            if User.objects.filter(user_id=user_id).exists():
                user = authenticate(request, username=user_id, password=password)
                if user is not None:
                    auth_login(request, user)

                    # Store user ID, first name, and last name in the session
                    request.session['user_id'] = user.user_id
                    request.session['first_name'] = user.first_name
                    request.session['last_name'] = user.last_name
                    
                    if(user.role.name == "Administrator"):
                        return redirect(request.GET.get('next', 'admin_redirect'))
                    else:
                        return redirect(request.GET.get('next', 'employee_dashboard')) 
                else:
                    messages.error(request, 'Invalid credentials. Please try again.')
            else:
                messages.error(request, 'User does not exist.')

    else:
        form = UserAuthenticationForm()

    clear_messages_view(request)

    return render(request, 'userauth/login.html', {'form': form})

def landing(request):
    return render(request, 'userauth/landingPage.html')

def index(request):
    return render(request, 'userauth/index.html')

def redirect_to_admin_dashboard(request):
    admin_url = reverse('admin:index')
    return redirect(admin_url)

def clear_messages_view(request):
    storage = messages.get_messages(request)
    storage.used = True
