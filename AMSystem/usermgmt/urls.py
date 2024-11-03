from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('success/', views.success_page, name='success_page'),  # Add this line
]