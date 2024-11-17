from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from .models import Role, Department, User, Account
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from django.utils.html import format_html
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class RoleAdmin(UnfoldModelAdmin):
    list_display = ('name', 'is_staff')
    search_fields = ('name',)
    list_filter = ('is_staff',)

class DepartmentAdmin(UnfoldModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class UserAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'email', 'role', 'department', 'is_staff', 'is_active', 'profile_picture_thumbnail')
    search_fields = ('user_id', 'first_name', 'last_name', 'email')
    list_filter = ('role', 'department', 'is_staff', 'is_active')

    fieldsets = (
        (None, {
            'fields': ('user_id', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'birthdate', 'contact_number', 'email', 'profile_image')
        }),
        ('Permissions', {
            'fields': ('role', 'department', 'is_staff', 'is_active')
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

    # Method to display profile image thumbnail in the admin list view
    def profile_picture_thumbnail(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="30" height="30" style="border-radius:50%;" />', obj.profile_image.url)
        return ""
    profile_picture_thumbnail.short_description = 'Profile Picture'

class AccountAdmin(UnfoldModelAdmin):
    list_display = ('user', 'password')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')

admin.site.register(Role, RoleAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
