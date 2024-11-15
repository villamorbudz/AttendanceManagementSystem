from django.urls import path
from . import views

urlpatterns = [
    path('admin/register/', views.register, name='register'),
]