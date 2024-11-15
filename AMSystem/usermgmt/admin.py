from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from .models import Role, Department, User
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm
from unfold.contrib.filters.admin import ( 
            RangeDateFilter,
            # RelatedFieldFilter,
            # DateFieldFilter,
            # BooleanFieldFilter,
        
        )

class RoleAdmin(UnfoldModelAdmin):
    list_display = ('name', 'is_staff', 'is_superuser')
    search_fields = ('name',)
    list_filter = ('is_staff', 'is_superuser') 

class DepartmentAdmin(UnfoldModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
# , ImportExportModelAdmin
class UserAdmin(UnfoldModelAdmin,ImportExportModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'email', 'department', 'is_staff', 'is_active')
    search_fields = ('user_id', 'first_name', 'last_name', 'email')
    list_filter = ('department', 'is_staff', 'is_active')
    fieldsets = (
        (None, {
            'fields': ('user_id', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'birthdate', 'contact_number', 'email')
        }),
        ('Permissions', {
            'fields': ('department', 'is_staff', 'is_active')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'password1', 'password2', 'first_name', 'last_name', 'birthdate', 'contact_number', 'email', 'role', 'department', 'is_staff', 'is_active'),
        }),
        ('created_at', RangeDateFilter)
    )
    ordering = ('user_id',)
    filter_horizontal = ()
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_filter_submit = True



class AccountAdmin(UnfoldModelAdmin):
    list_display = ('user', 'password')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')

admin.site.register(Role, RoleAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(User, UserAdmin)
