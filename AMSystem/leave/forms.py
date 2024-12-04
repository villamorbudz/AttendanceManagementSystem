from django import forms
from .models import LeaveRequest

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'leave_type','reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'leave_type': 'Leave Type',
            'reason': 'Reason',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')

        if start_date and start_date < cleaned_data.get('end_date'):
            raise forms.ValidationError("End date must be after the start date.")

        return cleaned_data

    def save(self, commit=True):
        leave_request = super().save(commit=False)
        leave_request.status = 'Pending'
        if commit:
            leave_request.save()
        return leave_request