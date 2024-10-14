from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
        #  login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to a success page
    else:
        form = UserRegistrationForm()
    return render(request, 'usermgmt/registration.html', {'form': form})
