from django.contrib import admin
from .models import User, Role, Department  

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'email', 'department', 'role', 
                    'contact_number', 'is_staff', 'is_active')
    search_fields = ('user_id', 'first_name', 'last_name', 'email', 'department__name', 
                        'role__name', 'is_staff', 'is_active')  # Use double underscores to search related fields

# Register User with the custom UserAdmin
admin.site.register(User, UserAdmin)

# Optionally, if you need to manage Roles and Departments
admin.site.register(Role)  # Register Role if you want to manage it from admin
admin.site.register(Department)
