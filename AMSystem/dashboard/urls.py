# dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
        path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
        path('employee_dashboard/profile/', views.emp_profile, name='emp_profile'),
        # path('login/', views.login_view, name='login'),
        # path('logout/', views.logout_view, name='logout'),
]