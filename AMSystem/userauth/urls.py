from django.urls import path
from . import views
from .views import login_view, register, access_denied

urlpatterns = [
    path('', views.index, name=""),
    path('login/', views.login_view, name='login'),
    path('home/', views.landing, name='home'),
    path('access-denied/', views.access_denied, name='access_denied'),
]
