import datetime
from decimal import Decimal
from django.http import HttpResponseBadRequest
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Level, Shape, Topping, Berry, Decor, Customer, Bake, Order, BakeCategory
from .forms import NewUserForm, ChangeUserDataForm


def index(request):
    if request.method == 'POST':
        bake = request.POST.get('BAKE')
        phone_number = request.POST.get('PHONE')
        email = request.POST.get('EMAIL')
        address = request.POST.get('ADDRESS')
        order_date = request.POST.get('DATE')
        order_time = request.POST.get('TIME')
        delivery_comment = request.POST.get('DELIVCOMMENTS')
        customer_name = request.POST.get('NAME')
        bake_levels = request.POST.get('LEVELS')
        bake_shape = request.POST.get('FORM')
        bake_topping = request.POST.get('TOPPING')
        bake_berry = request.POST.get('BERRIES')
        bake_decor = request.POST.get('DECOR')
        bake_words = request.POST.get('WORDS')
        order_comment = request.POST.get('COMMENTS')
        if not order_comment:
            order_comment = 'Позвонить за час'

        if not request.user.is_authenticated:
            if not email:
                return HttpResponseBadRequest()

            user = User.objects.filter(email=email).first()
            if not user:
                username, _ = email.split('@')
                password = 'Password123'  # dummy plug
                user = User(
                    username=username,
                    email=email,
                    password=email,
                )
                user.set_password(password)
                user.save()

                user.customer.first_name = customer_name
                user.customer.phone_number = phone_number
                user.customer.address = address
                user.save()

            login(request, user)

        customer = request.user.customer

        if bake:
            order_bake = Bake.objects.get(name=bake)
            order_sum = order_bake.get_price()
        else:
            order_shape_object = Shape.objects.get(id=bake_shape)
            order_level_object = Level.objects.get(id=bake_levels)
            order_topping_object = Topping.objects.get(id=bake_topping)
            order_berries_object = Berry.objects.get(id=bake_berry)
            order_decor_object = Decor.objects.get(id=bake_decor)

            order_bake = Bake.objects.create(
                name='Торт заказной',
                kind=True,
                title=bake_words,
                level=order_level_object,
                shape=order_shape_object,
                topping=order_topping_object,
                berries=order_berries_object,
                decor=order_decor_object
            )
            order_sum = order_bake.get_price()
            if bake_words:
                order_sum = order_sum + 500

        delivery_date = datetime.datetime.strptime(order_date, '%Y-%m-%d')
        min_delivery_date = datetime.datetime.now() + datetime.timedelta(days=1)
        if delivery_date < min_delivery_date:
            order_sum = order_sum * Decimal(1.2)

        Order.objects.create(
            bake=order_bake,
            customer=customer,
            comment=order_comment,
            delivery_address=address,
            delivery_date=order_date,
            delivery_time=order_time,
            total=order_sum,
        )
        return redirect('lk')

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
        template_name='index.html',
        context={
            'bake_elements': bake_elements,
            'bake_elements_json': bake_elements_json,
            'categories': BakeCategory.objects.all(),
        }
    )


@login_required
def lk(request):
    customer = Customer.objects.get(user=request.user)

    #  handle user info form
    if request.method == 'POST':
        form = ChangeUserDataForm(request.POST)
        if form.is_valid():
            customer.first_name = form.cleaned_data['first_name']
            customer.last_name = form.cleaned_data['last_name']
            customer.phone_number = form.cleaned_data['phone_number']
            customer.address = form.cleaned_data['address']
            customer.save()
            return redirect('lk')
    else:
        form = ChangeUserDataForm(
            initial={
                'first_name': request.user.customer.first_name,
                'last_name': request.user.customer.last_name,
                'phone_number': request.user.customer.phone_number,
                'address': request.user.customer.address,
            }
        )
    context = {
        'form': form,
        'orders': customer.orders.all(),
    }
    return render(request, 'lk/lk.html', context)


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('lk')
    form = NewUserForm()
    return render(request=request, template_name='registration/register.html', context={'register_form': form})


def catalog(request, category=None):
    bakes = Bake.objects.filter(kind=False)
    if category:
        bakes = bakes.filter(category=category)
        category = get_object_or_404(BakeCategory, pk=category)

    context = {
        'bakes': bakes,
        'current_category': category,
        'categories': BakeCategory.objects.all()
    }
    return render(request=request, template_name='catalog.html', context=context)


def make_catalog_order(request):
    bake = Bake.objects.get(pk=request.GET['bake'])

    context = {
        'bake': bake,
    }

    return render(request=request, template_name='make_catalog_order.html', context=context)
