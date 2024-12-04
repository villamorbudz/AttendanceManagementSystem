# dashboard/urls.py
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
]
