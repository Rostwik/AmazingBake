from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    phone_number = models.CharField(
        max_length=256,
        blank=True,
        default="",
        verbose_name="Номер телефона заказчика",
    )
    first_name = models.CharField(
        max_length=256,
        blank=True,
        default="",
        verbose_name="Имя заказчика",
    )
    last_name = models.CharField(
        max_length=256,
        blank=True,
        default="",
        verbose_name="Фамилия заказчика",
    )
    address = models.TextField(
        verbose_name="Адрес заказчика",
    )

    def __str__(self):
        return f"Заказчик {self.user.username} {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"


@receiver(post_save, sender=User)
def create_or_update_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
    instance.customer.save()


class Level(models.Model):
    name = models.CharField(
        max_length=256,
        blank=True,
        default='EMPTY',
        verbose_name="Уровни торта",
    )

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Цена уровня",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Количество уровней"
        verbose_name_plural = "Количество уровней"


class Shape(models.Model):
    name = models.CharField(
        max_length=256,
        blank=True,
        default='CIRCLE',
        verbose_name="Наименование формы",
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Цена формы",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Форма"
        verbose_name_plural = "Формы"


class Topping(models.Model):
    name = models.CharField(
        max_length=256,
        blank=True,
        default='WITHOUT',
        verbose_name="Наименование начинки",
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Цена топпинга",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Начинка"
        verbose_name_plural = "Начинки"


class Berry(models.Model):
    BERRY_CHOICES = [
        ('WITHOUT', 'Без ягод'),
        ('RASPBERRY', 'Малина'),
        ('BLUEBERRY', 'Голубика'),
        ('BlACKBERRY', 'Ежевика'),
        ('STRAWBERRY', 'Клубника'),
    ]
    name = models.CharField(
        max_length=256,
        blank=True,
        default='WITHOUT',
        choices=BERRY_CHOICES,
        verbose_name="Название ягоды",
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Цена ягоды",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ягода"
        verbose_name_plural = "Ягоды"


class Decor(models.Model):
    DECOR_CHOICES = [
        ('WITHOUT', 'Без декора'),
        ('PISTACHIO', ' Фисташки'),
        ('HAZELNUT', ' Фундук'),
        ('MERINQUE', 'Безе'),
        ('PECAN', 'Пекан'),
        ('MARSHMALLOW', 'Маршмеллоу'),
        ('MARZIPAN', 'Марципан'),
    ]
    name = models.CharField(
        max_length=256,
        blank=True,
        default='WITHOUT',
        choices=DECOR_CHOICES,
        verbose_name="Наименование декора",
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Цена декора",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Оформление"
        verbose_name_plural = "Оформление"


class BakeCategory(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=250,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"


class Bake(models.Model):
    name = models.TextField(
        "Название товарной позиции",
        blank=True,
    )
    description = models.TextField(
        'Описание торта',
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        BakeCategory,
        verbose_name="Категория",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    image = models.ImageField(
        'Изображение торта',
        upload_to='bakes/',
        null=True,
        blank = True,
    )
    kind = models.BooleanField(
        'Признак заказного торта',
        null=True,
    )
    title = models.TextField(
        verbose_name="Надпись на торте",
        blank=True,
    )
    level = models.ForeignKey(
        Level,
        verbose_name="Количество уровней",
        null=True,
        on_delete=models.SET_NULL,
    )
    shape = models.ForeignKey(
        Shape,
        verbose_name="Форма",
        null=True,
        on_delete=models.SET_NULL,
    )
    topping = models.ForeignKey(
        Topping,
        verbose_name="Топпинг",
        null=True,
        on_delete=models.SET_NULL,
    )
    berries = models.ForeignKey(
        Berry,
        verbose_name="Ягоды",
        null=True,
        on_delete=models.SET_NULL,
    )
    decor = models.ForeignKey(
        Decor,
        verbose_name="Декор",
        null=True,
        on_delete=models.SET_NULL,
    )


    def get_price(self):
        price = self.level.price + \
               self.shape.price + \
               self.topping.price + \
               self.berries.price + \
               self.decor.price
        return int(price)

    class Meta:
        verbose_name = "Торт"
        verbose_name_plural = "Торты"

    def __str__(self):
        return f"Торт: {self.name}"


class Order(models.Model):
    ORDER_STATUSES_CHOICES = [
        ('NEW', 'Создан'),
        ('PAID', 'Оплачен'),
        ('COOKING', 'Готовится'),
        ('IN_DELIVERY', 'В доставке'),
        ('DELIVERED', 'Доставлен'),
    ]
    bake = models.ForeignKey(
        Bake,
        related_name="orders",
        verbose_name="Торт",
        on_delete=models.PROTECT,
    )
    status = models.CharField(
        max_length=256,
        choices=ORDER_STATUSES_CHOICES,
        blank=True,
        default="NEW",
        verbose_name="Статус заказа",
    )
    customer = models.ForeignKey(
        Customer,
        related_name="orders",
        verbose_name="Заказчик",
        on_delete=models.PROTECT,
    )
    comment = models.TextField(
        verbose_name="Комментарий к заказу",
        blank=True,
    )
    delivery_address = models.TextField(
        verbose_name="Адрес доставки",
    )
    delivery_date = models.DateField(
        verbose_name="Дата доставки",
    )
    delivery_time = models.TimeField(
        verbose_name="Время доставки",
    )
    total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Стоимость заказа",
    )

    def __str__(self):
        return f"Заказ № {self.pk}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
