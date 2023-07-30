import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse

from .models import Order, Level, Shape, Topping, Berry, Decor, Bake, Customer, BakeCategory


def export_to_csv(modeladmin, request, queryset):
    """Возвращает файл с данными в формате CSV"""
    opts = modeladmin.model._meta
    content_disposition = 'attachment; filename=report.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [
        field for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d')
            data_row.append(value)
        writer.writerow(data_row)
    return response


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'bake', 'status', 'customer', 'comment',
        'delivery_address', 'delivery_date', 'delivery_time',
        'total',
    ]
    list_display_links = [
        'id', 'bake',
    ]
    actions = ['export_to_csv']

    @admin.action(description='Export to CSV')
    def export_to_csv(self, request, queryset):
        """Возвращает файл с данными в формате CSV"""
        opts = self.model._meta
        content_disposition = 'attachment; filename=orders.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = content_disposition
        writer = csv.writer(response)
        fields = [
            field for field in opts.get_fields()
            if not field.many_to_many and not field.one_to_many
        ]
        writer.writerow([field.verbose_name for field in fields])
        for obj in queryset:
            data_row = []
            for field in fields:
                value = getattr(obj, field.name)
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%Y-%m-%d')
                data_row.append(value)
            writer.writerow(data_row)
        return response


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    pass


@admin.register(Shape)
class ShapeAdmin(admin.ModelAdmin):
    pass


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Berry)
class BerryAdmin(admin.ModelAdmin):
    pass


@admin.register(Decor)
class DecorAdmin(admin.ModelAdmin):
    pass


@admin.register(Bake)
class BakeAdmin(admin.ModelAdmin):
    list_filter = ['kind']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(BakeCategory)
class BakeCategoryAdmin(admin.ModelAdmin):
    pass