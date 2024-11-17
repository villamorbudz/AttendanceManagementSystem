# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
        path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
        path('admin_dashboard/admin_employee_status/', views.admin_employee_status, name='admin_employee_status'),
        path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
        path('employee_dashboard/profile/', views.employee_profile, name='employee_profile'),
        path('profile/', views.employee_profile, name='employee_profile'), 

        # path('login/', views.login_view, name='login'),
        # path('logout/', views.logout_view, name='logout'),
]