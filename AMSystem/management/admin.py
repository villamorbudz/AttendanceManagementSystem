from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.forms import ImportForm, ExportForm
from django.utils.html import format_html
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from .models import Role, Department, User
from .forms import UserChangeForm, UserCreationForm

class RoleAdmin(UnfoldModelAdmin):
    list_display = ('name', 'is_staff', 'is_superuser')
    search_fields = ('name',)
    list_filter = ('is_staff', 'is_superuser') 

class DepartmentAdmin(UnfoldModelAdmin):
    list_display = ('name', 'get_roles')
    search_fields = ('name',)

    def get_roles(self, obj):
        return ", ".join([role.name for role in obj.role.all()])
    get_roles.short_description = 'Roles'


class UserAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'email', 'department', 'is_staff', 'is_active')
    search_fields = ('user_id', 'first_name', 'last_name', 'email')
    list_filter = ('department', 'is_staff', 'is_active')
    fieldsets = (
        (None, {
            'fields': ('user_id', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'birthdate', 'contact_number', 'email', 'profile_image')
        }),
        ('Permissions', {
            'fields': ('department', 'is_staff', 'is_active')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'first_name', 'last_name', 'birthdate', 'contact_number', 'email', 'role', 'department', 'is_staff', 'is_active', 'profile_image'),
        }),
    )

    add_form = UserCreationForm
    form = UserChangeForm
    ordering = ('user_id',)
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_filter_submit = True


admin.site.register(Role, RoleAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(User, UserAdmin)
