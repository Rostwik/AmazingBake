# Generated by Django 4.2.3 on 2023-07-30 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakeshopapp', '0008_bake_image_alter_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='bake',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание торта'),
        ),
    ]
