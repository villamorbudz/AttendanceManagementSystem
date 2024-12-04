from django.urls import path
from . import views

app_name = 'usermgmt'

urlpatterns = [
    path('admin/register/', views.register, name='register'),
]