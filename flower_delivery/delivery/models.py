from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=150, default='Букет', verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, verbose_name='Имя клиента')
    phone = models.CharField(max_length=30, verbose_name='Телефон')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return self.username