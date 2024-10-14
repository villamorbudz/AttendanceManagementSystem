from django.contrib import admin
from .models import Employee

# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'first_name', 'last_name', 'email', 'birthdate', 'contact_number']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['employee_id', 'first_name', 'last_name', 'birthdate']