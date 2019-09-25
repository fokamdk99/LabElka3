from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def log_in(request):
    return render(request, "login/login.html")

def sign_up(request):
    context = {
        'user_form': CustomUserCreationForm
    }
    return render(request, "login/signup.html")

def login_authenticate(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username = username, password = password)
    if user is not None:
        login(request, user)
        print(f'uzytkownik zautentyfikowany')
    return redirect('index')

def create_new_user(request):
    username = request.POST['username']
    password = request.POST['password']
    
    email = request.POST['email']
    new_user = User.objects.create_user(username=username, password=password, email=email)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    return redirect('index')

def log_out(request):
    logout(request)
    return redirect('index')