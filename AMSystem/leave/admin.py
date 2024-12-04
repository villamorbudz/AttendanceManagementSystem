from django.contrib import admin
from .models import LeaveType, LeaveRequest

# Register your models here.

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'leave_type', 'start_date', 'end_date', 'reason','status', 'remarks','created_at')
    list_filter = ('status', 'leave_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'reason')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Leave Details', {
            'fields': ('leave_type', 'start_date', 'end_date', 'reason')
        }),
        ('Status Information', {
            'fields': ('status', 'remarks')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
