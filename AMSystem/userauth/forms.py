from django import forms
from usermgmt.models import Employee

class UserAuthenticationForm(forms.Form):
    employee_id = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        return employee_id

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password
