from django.contrib import admin

from bakeshopapp.models import Order, Level, Shape, Topping, Berry, Decor, Cake, Customer


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Level)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Shape)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Topping)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Berry)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Decor)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_filter = ['kind']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
