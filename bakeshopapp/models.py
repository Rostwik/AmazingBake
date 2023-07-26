from django.db import models


class Customer(models.Model):
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
        return f"Заказчик {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"


class Level(models.Model):
    EMPTY = 'No'
    ONE = 'ON'
    TWO = 'TW'
    THREE = 'TH'
    LEVEL_CHOICES = [
        (EMPTY, 'Не выбрано'),
        (ONE, 'Один'),
        (TWO, 'Два'),
        (THREE, 'Три'),
    ]

    name = models.CharField(
        max_length=256,
        blank=True,
        default=EMPTY,
        choices=LEVEL_CHOICES,
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
    NOT_CHOSEN = 'NC'
    CIRCLE = 'CI'
    SQUARE = 'SQ'
    RECTANGLE = 'RE'
    FORMS_CHOICES = [
        (NOT_CHOSEN, 'Не выбрано'),
        (CIRCLE, 'Круг'),
        (SQUARE, 'Квадрат'),
        (RECTANGLE, 'Прямоугольник'),
    ]
    name = models.CharField(
        max_length=256,
        blank=True,
        choices=FORMS_CHOICES,
        default=NOT_CHOSEN,
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
    EMPTY = 'No'
    WITHOUT = 'WO'
    WHITE_SOUCE = 'WS'
    CARAMEL = 'CA'
    MAPLE = 'MA'
    BILBERRY = 'BB'
    WHITE_CHOCOLATE = 'WC'
    STRAWBERRY = 'ST'
    TOPPING_CHOICES = [
        (EMPTY, 'Не выбрано'),
        (WITHOUT, 'Без топпинга'),
        (WHITE_SOUCE, 'Белый соус'),
        (CARAMEL, 'Карамельный'),
        (MAPLE, 'Кленовый'),
        (BILBERRY, 'Черничный'),
        (WHITE_CHOCOLATE, 'Молочный шоколад'),
        (STRAWBERRY, 'Клубничный'),
    ]

    name = models.CharField(
        max_length=256,
        blank=True,
        default=EMPTY,
        choices=TOPPING_CHOICES,
        verbose_name="Наимнование топпинга",
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Цена топпинга",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Топпинг"
        verbose_name_plural = "Топпинг"


class Berry(models.Model):
    EMPTY = 'NC'
    WITHOUT = 'WO'
    RASPBERRY = 'RA'
    BLUEBERRY = 'BL'
    BlACKBERRY = 'BB'
    STRAWBERRY = 'ST'
    BERRY_CHOICES = [
        (EMPTY, 'Не выбрано'),
        (WITHOUT, 'Без ягод'),
        (RASPBERRY, 'Малина'),
        (BLUEBERRY, 'Голубика'),
        (BlACKBERRY, 'Ежевика'),
        (STRAWBERRY, 'Клубника'),
    ]
    name = models.CharField(
        max_length=256,
        blank=True,
        default=EMPTY,
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
    EMPTY = 'NC'
    WITHOUT = 'WO'
    PISTACHIO = 'PI'
    MERINQUE = 'ME'
    PECAN = 'PE'
    MARSHMALLOW = 'MM'
    MARZIPAN = 'MC'
    DECOR_CHOICES = [
        (EMPTY, 'Не выбрано'),
        (WITHOUT, 'Без декора'),
        (PISTACHIO, ' Фисташки'),
        (MERINQUE, 'Безе'),
        (PECAN, 'Пекан'),
        (MARSHMALLOW, 'Маршмеллоу'),
        (MARZIPAN, 'Марципан'),
    ]
    name = models.CharField(
        max_length=256,
        blank=True,
        default=EMPTY,
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
        verbose_name = "Декор"
        verbose_name_plural = "Декор"


class Order(models.Model):
    NEW = 'ne'
    PAID = 'PA'
    COOKING = 'CO'
    IN_DELIVERY = 'IND'
    DELIVERED = 'DE'

    ORDER_STATUSES_CHOICES = [
        (NEW, 'Создан'),
        (PAID, 'Оплачен'),
        (COOKING, 'Готовится'),
        (IN_DELIVERY, 'В доставке'),
        (DELIVERED, 'Доставлен'),
    ]

    status = models.CharField(
        max_length=256,
        choices=ORDER_STATUSES_CHOICES,
        blank=True,
        default="",
        verbose_name="Статус заказа",
    )
    customer = models.ForeignKey(
        Customer,
        related_name="customers",
        verbose_name="Заказчик",
        on_delete=models.PROTECT,
    )
    title = models.TextField(
        verbose_name="Надпись",
        blank=True,
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
    delivery_time = models.DateTimeField(
        verbose_name="Время доставки",
    )
    total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Стоимость заказа",
    )
    level = models.ForeignKey(
        Level,
        verbose_name="Количество уровней",
        null=True,
        on_delete=models.SET_NULL,
    )
    form = models.ForeignKey(
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

    def __str__(self):
        return f"Заказ № {self.pk}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
