from django.db import models
from django.utils import formats


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    weight = models.IntegerField(verbose_name='Вес')
    price = models.DecimalField(
        decimal_places=2, max_digits=5, verbose_name='Цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name


class Day(models.Model):
    day = models.DateField(verbose_name='День')
    dishes = models.ManyToManyField(Dish, verbose_name='Блюда')

    class Meta:
        verbose_name = 'День'
        verbose_name_plural = 'Дни'

    def __str__(self):
        return f"{formats.date_format(self.day)}"


class Order(models.Model):

    date = models.DateTimeField(verbose_name='Дата заказа')
    dishes = models.ManyToManyField(Dish, verbose_name='Заказ')
    client_id = models.CharField(max_length=100, verbose_name='ID клиента')
    address = models.CharField(max_length=100, verbose_name='Адрес доставки')
    completed = models.BooleanField(default=False, verbose_name='Выполнен')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'{self.address} клиент {self.client_id}'
