from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name=""),
    path('login/', views.login_view, name='login'),
    path('home/', views.landing, name='home')
]