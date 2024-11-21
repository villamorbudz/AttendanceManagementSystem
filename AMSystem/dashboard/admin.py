from django.contrib import admin
from .models import LeaveRequest, LeaveBalance

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    actions = ['approve_leave', 'deny_leave']

    def approve_leave(self, request, queryset):
        queryset.update(status='APPROVED')
        for leave in queryset:
            leave_balance = LeaveBalance.objects.get(employee=leave.employee)
            days_requested = (leave.end_date - leave.start_date).days + 1
            leave_balance.annual_leave_balance -= days_requested
            leave_balance.save()
        self.message_user(request, "Selected leaves approved and balance updated.")

    def deny_leave(self, request, queryset):
        queryset.update(status='DENIED')
        self.message_user(request, "Selected leaves denied.")

    approve_leave.short_description = "Approve selected leave requests"
    deny_leave.short_description = "Deny selected leave requests"

@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'annual_leave_balance')
