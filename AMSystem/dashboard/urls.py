# dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
        path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
        path('employee/dashboard/profile/', views.employee_profile, name='employee_profile'),
]