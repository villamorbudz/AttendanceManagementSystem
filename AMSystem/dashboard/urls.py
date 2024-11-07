# dashboard/urls.py

from django.urls import path
from . import views
from userauth.views import redirect_to_admin_dashboard

urlpatterns = [
        path('admin/redirect', redirect_to_admin_dashboard, name='admin_redirect'),
        path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
]