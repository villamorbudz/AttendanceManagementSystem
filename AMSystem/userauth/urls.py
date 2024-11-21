# userauth/urls.py
from django.urls import path
from . import views

app_name = 'userauth'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.index, name="index"),
    path('landing/', views.landing, name='landing'),
    # path('home/', views.landing, name='home'),
]