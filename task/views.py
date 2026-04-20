from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.db import IntegrityError


# Create your views here.
def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponse("User created successfully.")
            except IntegrityError:
                return HttpResponse("Failed to create user.")
        return render(request, "signup.html", {"form": form})

    return render(request, "signup.html", {"form": UserCreationForm()})
