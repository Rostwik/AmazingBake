from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import NewUserForm
from .models import Level, Shape, Topping, Berry, Decor


def index(request):
    print((request.GET))
    bake_elements = {
        'levels': Level.objects.all(),
        'shapes': Shape.objects.all(),
        'toppings': Topping.objects.all(),
        'berries': Berry.objects.all(),
        'decors': Decor.objects.all()
    }
    bake_elements_json = {
        'level_names': {item.id: item.name for item in bake_elements['levels']},
        'level_prices': {item.id: int(item.price) for item in bake_elements['levels']},
        'shape_names': {item.id: item.name for item in bake_elements['shapes']},
        'shape_prices': {item.id: int(item.price) for item in bake_elements['shapes']},
        'topping_names': {item.id: item.name for item in bake_elements['toppings']},
        'topping_prices': {item.id: int(item.price) for item in bake_elements['toppings']},
        'berry_names': {item.id: item.name for item in bake_elements['berries']},
        'berry_prices': {item.id: int(item.price) for item in bake_elements['berries']},
        'decor_names': {item.id: item.name for item in bake_elements['decors']},
        'decor_prices': {item.id: int(item.price) for item in bake_elements['decors']},
    }

    return render(
        request,
        template_name="index.html",
        context={
            'bake_elements': bake_elements,
            'bake_elements_json': bake_elements_json
        }
    )


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
