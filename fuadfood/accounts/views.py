from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm


# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print (username,password)#remove this!!
        user = authenticate(request, username=username,
                            password=password)
        if user is None:
            context = {"error":"Inavlid username or password"}
            return render(request, "accounts/login.html", context)
        login(request, user)
        return redirect('/')
    return render(request, "accounts/login.html", {})
def signup_view(request):
        form= UserCreationForm(request.POST or None)
        if form.is_valid():
            user_obj=form.save()
            return redirect ('/login')
        context = {"form":form}
        return render (request, "accounts/signup.html",context)

def logout_view(request):
        if request.method == 'POST':
                logout(request)
        return render(request,"accounts/logout.html")

