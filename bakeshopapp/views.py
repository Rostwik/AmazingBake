from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def lk(request):
    return render(request, "base_lk.html")