from django.shortcuts import render

# Create your views here.
def home(request):
 
 return render(request, 'crm/index.html')

def login_view(request):
    return render(request, 'crm/login.html')  # Make sure 'login.html' matches the filename

def dashboard_view(request):
    return render(request, 'crm/dashboard.html')

