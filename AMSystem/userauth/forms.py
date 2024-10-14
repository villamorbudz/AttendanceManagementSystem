from django import forms
from django.contrib.auth.forms import AuthenticationForm
from usermgmt.models import User

def login(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            user = authenticate(request, user_id=user_id, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a success page
    else:
        form = UserAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})