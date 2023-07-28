import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings

from .models import Link
from .bitly_service import get_count_clicks, is_bitlink


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'description', 'url', 'bitlink',
        'count_clicks_a_day', 'count_clicks_week',
        'count_clicks_month', 'active', 'created_at',
    ]
    list_display_links = ['title', ]
    list_filter = ['active', ]
    search_fields = ['title', ]
    fields = [
        'title', 'url', 'bitlink', 'description',
        'active', 'created_at', 'updated_at',
    ]
    readonly_fields = ['bitlink', 'created_at', 'updated_at']
    actions = ['export_to_csv', ]

    @admin.action(description='Export to CSV')
    def export_to_csv(self, request, queryset):
        """Возвращает файл с данными в формате CSV"""
        token = settings.BITLY_TOKEN
        opts = self.model._meta
        content_disposition = 'attachment; filename=referals.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = content_disposition
        writer = csv.writer(response)
        fields = [
            field for field in opts.get_fields()
            if not field.many_to_many and not field.one_to_many
        ]
        headers = [field.verbose_name for field in fields] \
                  + ['клики за день', 'клики за неделю', 'клики за месяц']
        writer.writerow(headers)
        for obj in queryset:
            data_row = []
            for field in fields:
                value = getattr(obj, field.name)
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%Y-%m-%d')
                data_row.append(value)
            if is_bitlink(token, obj.bitlink):
                data_row.extend(
                    [
                        get_count_clicks(
                            token, obj.bitlink, 'day'),
                        get_count_clicks(
                            token, obj.bitlink, 'week'),
                        get_count_clicks(
                            token, obj.bitlink, 'month')
                    ]
                )
            writer.writerow(data_row)
        return response
