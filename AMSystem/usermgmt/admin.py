from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'role')
    search_fields = ('first_name', 'last_name', 'email')

    def role(self, obj):
        return 'Admin' if obj.is_superuser else 'Employee'
    role.short_description = 'Role'

# Register the Group model
admin.site.unregister(Group)
admin.site.register(Group)
