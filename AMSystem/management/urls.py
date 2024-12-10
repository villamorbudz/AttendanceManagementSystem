from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('bulk-register/', views.bulk_register, name='bulk_register'),
    path('bulk-attendance/', views.bulk_attendance, name='bulk_attendance'),
    path('bulk-leave-requests/', views.bulk_leave_requests, name='bulk_leave_requests'),
    path('success/', views.success_page, name='success'),
]