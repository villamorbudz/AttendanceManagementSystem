from django.urls import path
from. import views

urlpatterns = [
    path('', views.home, name=""),
    path('login/', views.login_view, name='login),
]