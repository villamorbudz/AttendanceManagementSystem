from django import forms
from django.core.exceptions import ValidationError
from .models import Employee

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'department', 'email', 'birthdate', 'contact_number']

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        if Employee.objects.filter(employee_id=employee_id).exists():
            raise ValidationError("Error: Employee ID already in use.")
        return employee_id

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Employee.objects.filter(email=email).exists():
            raise ValidationError("Email address already in use. Please use a different email.")
        return email

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if contact_number and Employee.objects.filter(contact_number=contact_number).exists():
            raise ValidationError("Contact number already in use. Please use a different contact number.")
        return contact_number
