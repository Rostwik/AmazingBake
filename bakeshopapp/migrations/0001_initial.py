# Generated by Django 4.2.3 on 2023-07-27 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Berry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, choices=[('WITHOUT', 'Без ягод'), ('RASPBERRY', 'Малина'), ('BLUEBERRY', 'Голубика'), ('BlACKBERRY', 'Ежевика'), ('STRAWBERRY', 'Клубника')], default='WITHOUT', max_length=256, verbose_name='Название ягоды')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Цена ягоды')),
            ],
            options={
                'verbose_name': 'Ягода',
                'verbose_name_plural': 'Ягоды',
            },
        ),
        migrations.CreateModel(
            name='Cake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, verbose_name='Название товарной позиции')),
                ('kind', models.BooleanField(null=True, verbose_name='Признак заказного торта')),
                ('title', models.TextField(blank=True, verbose_name='Надпись на торте')),
                ('berries', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bakeshopapp.berry', verbose_name='Ягоды')),
            ],
            options={
                'verbose_name': 'Торт',
                'verbose_name_plural': 'Торты',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, default='', max_length=256, verbose_name='Номер телефона заказчика')),
                ('first_name', models.CharField(blank=True, default='', max_length=256, verbose_name='Имя заказчика')),
                ('last_name', models.CharField(blank=True, default='', max_length=256, verbose_name='Фамилия заказчика')),
                ('address', models.TextField(verbose_name='Адрес заказчика')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заказчик',
                'verbose_name_plural': 'Заказчики',
            },
        ),
        migrations.CreateModel(
            name='Decor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, choices=[('WITHOUT', 'Без декора'), ('PISTACHIO', ' Фисташки'), ('HAZELNUT', ' Фундук'), ('MERINQUE', 'Безе'), ('PECAN', 'Пекан'), ('MARSHMALLOW', 'Маршмеллоу'), ('MARZIPAN', 'Марципан')], default='WITHOUT', max_length=256, verbose_name='Наименование декора')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Цена декора')),
            ],
            options={
                'verbose_name': 'Оформление',
                'verbose_name_plural': 'Оформление',
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, choices=[('ONE', 'Один'), ('TWO', 'Два'), ('THREE', 'Три')], default='EMPTY', max_length=256, verbose_name='Уровни торта')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Цена уровня')),
            ],
            options={
                'verbose_name': 'Количество уровней',
                'verbose_name_plural': 'Количество уровней',
            },
        ),
        migrations.CreateModel(
            name='Shape',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, choices=[('CIRCLE', 'Круг'), ('SQUARE', 'Квадрат'), ('RECTANGLE', 'Прямоугольник')], default='CIRCLE', max_length=256, verbose_name='Наименование формы')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Цена формы')),
            ],
            options={
                'verbose_name': 'Форма',
                'verbose_name_plural': 'Формы',
            },
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, choices=[('WITHOUT', 'Без начинки'), ('WHITE_SOUCE', 'Белый соус'), ('CARAMEL', 'Карамельный'), ('MAPLE', 'Кленовый'), ('BILBERRY', 'Черничный'), ('WHITE_CHOCOLATE', 'Молочный шоколад'), ('STRAWBERRY', 'Клубничный')], default='WITHOUT', max_length=256, verbose_name='Наименование начинки')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Цена топпинга')),
            ],
            options={
                'verbose_name': 'Начинка',
                'verbose_name_plural': 'Начинки',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('NEW', 'Создан'), ('PAID', 'Оплачен'), ('COOKING', 'Готовится'), ('IN_DELIVERY', 'В доставке'), ('DELIVERED', 'Доставлен')], default='NEW', max_length=256, verbose_name='Статус заказа')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий к заказу')),
                ('delivery_address', models.TextField(verbose_name='Адрес доставки')),
                ('delivery_date', models.DateField(verbose_name='Дата доставки')),
                ('delivery_time', models.DateTimeField(verbose_name='Время доставки')),
                ('total', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Стоимость заказа')),
                ('cake', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='bakeshopapp.cake', verbose_name='Торт')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customers', to='bakeshopapp.customer', verbose_name='Заказчик')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.AddField(
            model_name='cake',
            name='decor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bakeshopapp.decor', verbose_name='Декор'),
        ),
        migrations.AddField(
            model_name='cake',
            name='form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bakeshopapp.shape', verbose_name='Форма'),
        ),
        migrations.AddField(
            model_name='cake',
            name='level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bakeshopapp.level', verbose_name='Количество уровней'),
        ),
        migrations.AddField(
            model_name='cake',
            name='topping',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bakeshopapp.topping', verbose_name='Топпинг'),
        ),
    ]
