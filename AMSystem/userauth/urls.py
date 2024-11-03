from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('home/', views.landing, name='home'),
    path('access-denied/', views.access_denied, name='access_denied'),
    path('register/', views.register, name='register'),  # Ensure the register view is included
=======
  path('', views.index, name='index'),
  path('login/', views.index, name='index'),
>>>>>>> 43e58055dc4f399f298c567cdd630f3f495d2045
]