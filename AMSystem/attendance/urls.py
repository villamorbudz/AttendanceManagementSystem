from django.urls import path
from . import views

urlpatterns = [
    path('record_attendance/', views.record_attendance, name='record_attendance'),
]
