from django.urls import path
from .views import record_attendance

urlpatterns = [
    path('record/', record_attendance, name='record_attendance'),
]
