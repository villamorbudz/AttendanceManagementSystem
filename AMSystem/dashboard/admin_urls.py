# dashboard/admin_urls.py
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from . import views

app_name = 'admin_dashboard'  # Ensure the app_name is properly set


urlpatterns = [
    # path('', views.admin_dashboard, name='admin_dashboard'),  # Root route for admin_dashboard
    # path('employee/status/', views.admin_employee_status, name='admin_employee_status'),
    # path('leave/management/', views.admin_leave_management, name='admin_leave_management'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Fix double slash
    path('employee/status/', views.admin_employee_status, name='admin_employee_status'),
    path('leave/management/', views.admin_leave_management, name='admin_leave_management'),

]
