from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('home/', views.landing, name='home'),
    path('access-denied/', views.access_denied, name='access_denied'),
    path('register/', views.register, name='register'),  # Ensure the register view is included
]