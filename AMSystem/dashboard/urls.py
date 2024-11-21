# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'employee_dashboard'

urlpatterns = [
    # # Admin Dashboard URLs
    # path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # path('admin/employee/status/', views.admin_employee_status, name='admin_employee_status'),
    # path('admin/leave/management/', views.admin_leave_management, name='admin_leave_management'),
    
    # Employee Dashboard URLs
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/profile/', views.employee_profile, name='employee_profile'),
    path('employee/leave/request/', views.request_leave, name='request_leave'),
    path('employee/leave/status/', views.leave_status, name='leave_status'),
    path('employee/leave/balance/', views.leave_balance, name='leave_balance'),
    
    # Corrected path to match the view name
    path('employee/leave/request/dashboard/', views.employee_leave_request_dashboard, name='employee_leave_request_dashboard'),
    
    path('employee/submit/leave/request/', views.submit_leave_request, name='submit_leave_request'),
]
