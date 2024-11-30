from django.contrib import admin
from .models import Attendance

# Register your models here.
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_department', 'date', 'time_in', 'time_out', 'status')
    search_fields = ('user__username', 'date')
    list_filter = ('status',)

    def get_department(self, obj):
        return obj.user.department.name
    get_department.short_description = 'Department'  # Column header in admin
    get_department.admin_order_field = 'user__department__name'  # Enable sorting

admin.site.register(Attendance, AttendanceAdmin)