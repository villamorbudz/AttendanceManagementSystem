from django.urls import path
from . import views

app_name = 'leave'

urlpatterns = [
    path('employee/leave/request/', views.leave_request, name='leave_request'),
]