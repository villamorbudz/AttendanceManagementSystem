from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

class UserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('user_id', 'password')
