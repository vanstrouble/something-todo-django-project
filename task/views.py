from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import TaskForm


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


@login_required(login_url="login")
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            try:
                task.save()
                return redirect("tasks")
            except IntegrityError:
                form.add_error(None, "Failed to create task. Please try again.")
    else:
        form = TaskForm()

    return render(request, "create_task.html", {"form": form})
