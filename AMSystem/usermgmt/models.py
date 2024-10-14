from django.contrib.auth.models import AbstractUser
from django.db import models

class Employee(AbstractUser):
    username = 'none'
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    birthdate = models.DateField()
    contact_number = models.CharField(max_length=100)

    USERNAME_FIELD = 'employee_id'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    groups = None
    user_permissions = None
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.employee_id})"
