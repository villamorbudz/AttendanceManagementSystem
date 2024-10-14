from django import forms
from .models import Employee

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'birthdate', 'contact_number', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password
