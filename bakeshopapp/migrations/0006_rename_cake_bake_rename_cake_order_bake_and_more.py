# Generated by Django 4.2.3 on 2023-07-29 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakeshopapp', '0005_merge_20230729_1844'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cake',
            new_name='Bake',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='cake',
            new_name='bake',
        ),
        migrations.AlterField(
            model_name='level',
            name='name',
            field=models.CharField(blank=True, default='EMPTY', max_length=256, verbose_name='Уровни торта'),
        ),
    ]
