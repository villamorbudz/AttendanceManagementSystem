from django.urls import path
from . import views
from usermgmt.views import register


urlpatterns = [
    path('', views.home, name=""),
    path('login/', views.login, name='login'),
]