# dashboard/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def manager_dashboard(request):
    try:
        if request.user.department.role.first().name != 'Manager':
            return redirect('dashboard:employee_dashboard')
    except AttributeError:
        return redirect('userauth:login')
    return render(request, 'dashboard/manager_dashboard.html')

@login_required
def employee_dashboard(request):
    try:
        if request.user.department.role.first().name != 'Employee':
            return redirect('dashboard:manager_dashboard')
    except AttributeError:
        return redirect('userauth:login')
    return render(request, 'dashboard/employee_dashboard.html')