from django.urls import path
from . import views
from management import views as management_views

app_name = 'dashboard'

urlpatterns = [
    # Common views
    path('', views.dashboard_home, name='home'),
    
    # Employee views
    path('employee/dashboard', views.employee_dashboard, name='employee_dashboard'),
    path('employee/profile/', views.employee_profile, name='employee_profile'),
    path('employee/attendance/', views.employee_attendance, name='employee_attendance'),
    path('employee/leave/', views.employee_leave, name='employee_leave'),
    path('employee/profile/update/', views.update_profile, name='update_profile'),
    path('employee/change-password/', views.change_password, name='change_password'),
    
    # Manager views
    path('management/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('management/profile/', views.manager_profile, name='manager_profile'),
    path('management/users/', views.manager_user_management, name='manager_user_management'),
    path('management/departments/', views.manager_departments, name='manager_departments'),
    path('management/roles/', views.manager_roles, name='manager_roles'),
    path('management/leave-types/', views.manager_leave_types, name='manager_leave_types'),
    
    # User management endpoints
    path('management/users/update/', views.update_user, name='update_user'),
    path('management/users/delete/', views.delete_user, name='delete_user'),
    path('management/users/restore/', views.restore_user, name='restore_user'),
    path('management/users/get_info/<str:user_id>/', views.get_user_info, name='get_user_info'),
    
    # Department Management URLs (linked to dashboard.views)
    path('departments/', views.department_management, name='department_management'),
    path('departments/add/', views.add_department, name='add_department'),
    path('departments/<int:department_id>/update/', views.update_department, name='update_department'),
    path('departments/<int:department_id>/delete/', views.delete_department, name='delete_department'),
    path('departments/<int:department_id>/restore/', management_views.department_restore, name='restore_department'),
    
    # API endpoints
    path('api/chart-data/', views.get_chart_data, name='chart_data'),
    path('api/users/<int:user_id>/', views.get_user_data, name='get_user_data'),
]
