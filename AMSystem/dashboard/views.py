# dashboard/views.py

from django.shortcuts import render

def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')

def employee_dashboard(request):
    return render(request, 'dashboard/employee_dashboard.html')

def employee_profile(request):
    return render(request, 'dashboard/employee_profile.html')
