from bakeshopapp.admin import export_to_csv
from django.contrib import admin

from .models import Link


# Register your models here.
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'description', 'url', 'bitlink',
        'count_clicks_a_day', 'count_clicks_week',
        'count_clicks_month', 'active',
    ]
    list_display_links = ['id', 'title', ]
    list_filter = ['active', ]
    search_fields = ['title', ]
    fields = [
        'title', 'url', 'bitlink', 'description',
        'active', 'created_at', 'updated_at',
    ]
    readonly_fields = ['created_at', 'updated_at']
    actions = [export_to_csv]

    export_to_csv.short_description = 'Export to CSV'
