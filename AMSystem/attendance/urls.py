from django.urls import path
from . import views

urlpatterns = [
    path('attendance/record/', views.record_attendance, name='record_attendance'),
]
