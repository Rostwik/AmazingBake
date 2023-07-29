import datetime

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Level, Shape, Topping, Berry, Decor, Customer, Bake, Order
from .forms import NewUserForm, ChangeUserDataForm

def index(request):

    phone = request.GET.get('PHONE')
    email = request.GET.get('EMAIL')
    address = request.GET.get('ADDRESS')
    order_date = request.GET.get('DATE')
    order_time = request.GET.get('TIME')
    delivery_comment = request.GET.get('DELIVCOMMENTS')
    customer_name = request.GET.get('NAME')
    bake_levels = request.GET.get('LEVELS')
    bake_shape = request.GET.get('FORM')
    bake_topping = request.GET.get('TOPPING')
    bake_berry = request.GET.get('BERRIES')
    bake_decor = request.GET.get('DECOR')
    bake_words = request.GET.get('WORDS')
    order_comment = request.GET.get('COMMENTS')

    if phone:
        customer = Customer.objects.filter(phone_number=phone)
        if customer:
            customer = customer[0]
        else:
            username, _ = email.split('@')
            try:
                user = User.objects.create(
                    username=username,
                    email=email,
                    password=email,
                    first_name=customer_name
                )
                customer = Customer.objects.create(
                    user=user,
                    phone_number=phone,
                    first_name=customer_name,
                    last_name=customer_name,
                    address=address)
            except IntegrityError:
                user = User.objects.all()[0]
                customer = Customer.objects.create(
                    user=user,
                    phone_number=phone,
                    first_name=customer_name,
                    last_name=customer_name,
                    address=address)

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
            prices = [
                order_level_object.price,
                order_shape_object.price,
                order_topping_object.price,
                order_berries_object.price,
                order_decor_object.price
            ]
            order_sum = sum(prices)
            if bake_words:
                order_sum = order_sum + 500
            delivery_date = datetime.datetime.strptime(order_date, '%Y-%m-%d')
            min_delivery_date = datetime.datetime.now() + datetime.timedelta(days=1)
            if delivery_date < min_delivery_date:
                order_sum = order_sum * 1.2

            Order.objects.create(
                bake=order_bake,
                customer=customer,
                comment=order_comment,
                delivery_address=address,
                delivery_date=order_date,
                delivery_time=order_time,
                total=order_sum
            )

    print(request.GET)
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
            'bake_elements_json': bake_elements_json
        }
    )


@login_required
def lk(request):
    customer = Customer.objects.get(user=request.user)
    print(customer.orders.all())

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
            # messages.success(request, 'Вы успешно зарегистрировались.')
            return redirect('lk')
        messages.error(request, 'Не удалось зарегистрироваться.')
    form = NewUserForm()
    return render(request=request, template_name='registration/register.html', context={'register_form': form})
