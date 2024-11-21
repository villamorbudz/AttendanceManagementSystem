"""
URL configuration for AMSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import admin_dashboard
from dashboard import views

urlpatterns = [
<<<<<<< HEAD
    path('admin/dashboard', admin.site.urls, name="admin_dashboard"),
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
    path('', include('attendance.urls')),
    path('', include('dashboard.urls')),
    path('', include('userauth.urls')),
    path('', include('usermgmt.urls')),
=======
    path('admin/', admin.site.urls),  # Django admin
    # path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/', include('dashboard.admin_urls')),  # Admin-specific URLs
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
    path('', include('attendance.urls')),  # Main attendance URLs
    path('', include('dashboard.urls')),    # Dashboard URLs
    path('', include('userauth.urls')),     # Authentication URLs
    path('', include('usermgmt.urls')),     # User management URLs
>>>>>>> eadashboard
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
