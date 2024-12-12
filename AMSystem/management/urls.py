from django.urls import path
from . import views
from leave import views as leave_views
app_name = 'management'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('bulk-register/', views.bulk_register, name='bulk_register'),
    path('bulk-attendance/', views.bulk_attendance, name='bulk_attendance'),
    path('bulk-leave-requests/', views.bulk_leave_requests, name='bulk_leave_requests'),
    path('leave-request/<int:request_id>/update/',leave_views.leave_request_update, name='leave_request_update'),
    path('success/', views.success_page, name='success'),
]