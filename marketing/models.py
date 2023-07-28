from django.db import models
from django.conf import settings
from .bitly_service import get_short_link, get_count_clicks, is_bitlink


# Create your models here.
class Link(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='название')
    url = models.URLField(
        unique=True, verbose_name='ссылка')
    bitlink = models.URLField(
        verbose_name='битлинк',
        blank=True, null=True)
    description = models.TextField(
        blank=True, null=True,
        verbose_name='описание')
    active = models.BooleanField(default=True, verbose_name='ссылка активна')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='обновлена')

    def count_clicks_a_day(self):
        token = settings.BITLY_TOKEN
        if is_bitlink(token, self.bitlink):
            return get_count_clicks(
                token, self.bitlink, 'day')

    def count_clicks_week(self):
        token = settings.BITLY_TOKEN
        if is_bitlink(token, self.bitlink):
            return get_count_clicks(
                token, self.bitlink, 'week')

    def count_clicks_month(self):
        token = settings.BITLY_TOKEN
        if is_bitlink(token, self.bitlink):
            return get_count_clicks(
                token, self.bitlink, 'month')

    count_clicks_a_day.short_description = 'Клики за день'
    count_clicks_week.short_description = 'Клики за неделю'
    count_clicks_month.short_description = 'Клики за месяц'

    def save(self):
        self.bitlink = get_short_link(
            settings.BITLY_TOKEN, self.url
        )
        return super().save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'реферальная ссылка'
        verbose_name_plural = 'реферальные ссылки'
