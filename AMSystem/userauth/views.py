from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'userauth/index.html')

def login(request):
    return render(request, 'userauth/login.html')


