from django.contrib import admin

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'phonenumber', 'address', 'restaurant')
