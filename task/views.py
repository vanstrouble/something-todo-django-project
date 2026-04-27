from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from .forms import TaskForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import Task


# Create your views here.
def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
            except IntegrityError:
                form.add_error(None, "Failed to create user. Please try again.")
                return render(request, "signup.html", {"form": form})

            auth_login(request, user)
            return redirect("tasks")
        return render(request, "signup.html", {"form": form})

    return render(request, "signup.html", {"form": CustomUserCreationForm()})


@login_required(login_url="login")
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    completed_tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False
    ).order_by("-datecompleted")
    return render(
        request,
        "tasks.html",
        {"tasks": tasks, "completed_tasks": completed_tasks},
    )


def logout(request):
    auth_logout(request)
    return redirect("home")


def login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("tasks")
    else:
        form = CustomAuthenticationForm(request)

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


@login_required(login_url="login")
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_detail", task_id=task_id)
        return render(
            request,
            "task_template.html",
            {"task": task, "form": form, "is_editing": True},
        )

    is_editing = request.GET.get("edit") == "1"
    form = TaskForm(instance=task) if is_editing else None

    return render(
        request,
        "task_template.html",
        {"task": task, "form": form, "is_editing": is_editing},
    )


@login_required(login_url="login")
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        if task.datecompleted:
            task.datecompleted = None
        else:
            task.datecompleted = timezone.now()
        task.save(update_fields=["datecompleted"])

    return redirect("tasks")


@login_required(login_url="login")
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        task.delete()
        return redirect("tasks")

    return redirect("task_detail", task_id=task_id)
