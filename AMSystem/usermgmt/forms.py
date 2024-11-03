from django import forms
from .models import User, Department

class UserRegistrationForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        widget=forms.Select(attrs={'class': 'input input-bordered'}),
    )

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'birthdate', 'contact_number', 'email', 'department']
