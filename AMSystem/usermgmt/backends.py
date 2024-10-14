from django.contrib.auth.backends import ModelBackend
from .models import Employee

class EmployeeBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            employee = Employee.objects.get(employee_id=username)
        except Employee.DoesNotExist:
            return None
        
        if employee.check_password(password):
            return employee
        return None
