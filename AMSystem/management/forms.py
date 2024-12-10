from django import forms
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm, UserCreationForm as BaseUserCreationForm
from .models import User, Department

class UserRegistrationForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        widget=forms.Select(attrs={'class': 'input input-bordered'}),
    )

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'contact_number', 'department', 'birthdate']
        widgets = {
            'user_id': forms.TextInput(attrs={'class': 'input input-bordered'}),
            'contact_number': forms.TextInput(attrs={'class': 'input input-bordered'}),
            'birthdate': forms.DateInput(attrs={'class': 'input input-bordered', 'type': 'date'})
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'birthdate', 'contact_number', 'email', 'department']
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True}),
        }

class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'department')