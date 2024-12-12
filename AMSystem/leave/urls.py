from django.urls import path
from . import views

app_name = 'leave'

urlpatterns = [
    path('employee/leave/request/', views.leave_request, name='leave_request'),
    path('employee/leave/request/<int:request_id>/update/', views.leave_request_update, name='leave_request_update'),
    path('employee/leave/request/<int:request_id>/<str:action>/', views.process_leave_request, name='process_leave_request'),
]