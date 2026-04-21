from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.db import IntegrityError


# Create your views here.
def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
            except IntegrityError:
                form.add_error(None, "Failed to create user. Please try again.")
                return render(request, "signup.html", {"form": form})

            auth_login(request, user)
            return redirect("tasks")
        return render(request, "signup.html", {"form": form})

    return render(request, "signup.html", {"form": UserCreationForm()})


def tasks(request):
    return render(request, "tasks.html")


def logout(request):
    auth_logout(request)
    return redirect("home")


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("tasks")
    else:
        form = AuthenticationForm(request)

    return render(request, "login.html", {"form": form})
