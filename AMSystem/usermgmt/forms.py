from django import forms
from .models import User, Department
from .models import User

class UserRegistrationForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        widget=forms.Select(attrs={'class': 'input input-bordered'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'department']  # Removed 'username'
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input input-bordered'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'birthdate', 'contact_number', 'email', 'department']
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True}),
        }
