from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    
    # Manager routes
    path('management/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('management/profile/', views.manager_profile, name='manager_profile'),
    path('management/users/', views.manager_user_management, name='manager_user_management'),
    path('management/departments/', views.manager_departments, name='manager_departments'),
    path('management/roles/', views.manager_roles, name='manager_roles'),
    path('management/leave-types/', views.manager_leave_types, name='manager_leave_types'),
    
    # Employee routes
    path('employee/dashboard', views.employee_dashboard, name='employee_dashboard'),
    path('employee/profile/', views.employee_profile, name='employee_profile'),
    path('employee/attendance/', views.employee_attendance, name='employee_attendance'),
    path('employee/leave/', views.employee_leave, name='employee_leave'),
    
    # API routes
    path('api/chart-data/', views.get_chart_data, name='chart_data'),
]
