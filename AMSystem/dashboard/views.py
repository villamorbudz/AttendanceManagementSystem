# dashboard/views.py
from django.shortcuts import render
# from django.shortcuts import render, redirect
# from django.contrib.auth import logout
# from django.shortcuts import redirect

# def login_view(request):
#     return render(request, 'userauth/login.html')

# def logout_view(request):
#     logout(request)
#     return redirect('login')

# def admin_dashboard(request):
#     return render(request, 'dashboard/admin_dashboard.html')

def employee_dashboard(request):
    return render(request, 'dashboard/employee_dashboard.html')
def emp_profile(request):
    return render(request, 'dashboard/emp_profile.html')

