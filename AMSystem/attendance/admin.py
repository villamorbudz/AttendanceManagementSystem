from django.contrib import admin
from .models import Attendance

# Register your models here.
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('get_user_id', 'user', 'get_department', 'date', 'time_in', 'time_out', 'status')
    search_fields = ('user__username', 'user__user_id', 'date')
    list_filter = ('status',)

    def get_department(self, obj):
        return obj.user.department.name
    get_department.short_description = 'Department'  # Column header in admin
    get_department.admin_order_field = 'user__department__name'  # Enable sorting

    def get_user_id(self, obj):
        return obj.user.user_id
    get_user_id.short_description = 'User ID'  # Column header in admin
    get_user_id.admin_order_field = 'user__user_id'  # Enable sorting

admin.site.register(Attendance, AttendanceAdmin)