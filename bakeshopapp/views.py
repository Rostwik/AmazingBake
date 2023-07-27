from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages


def index(request):
    return render(request, "index.html")

def lk(request):
    return render(request, "base_lk.html")

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # messages.success(request, "Вы успешно зарегистрировались.")
            return redirect("lk")
        messages.error(request, "Не удалось зарегистрироваться.")
    form = NewUserForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})
