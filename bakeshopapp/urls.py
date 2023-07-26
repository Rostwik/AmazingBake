from django.urls import path

from bakeshopapp import views

urlpatterns = [
    path('', views.index),
]
