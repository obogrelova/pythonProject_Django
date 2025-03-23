from django.db import models

# Create your models here.

class Product(models.Model):
    bouquet = models.CharField(verbose_name='Букет', max_length=150)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', blank=True, null=True)

    def __str__(self):
        return self.bouquet


class Order(models.Model):
    bouquet = models.CharField(verbose_name='Букет', max_length=150)
    username = models.CharField(verbose_name='Имя клиента', max_length=150)
    phone = models.CharField(verbose_name='Телефон клиента', max_length=30)

    def __str__(self):
        return f'Заказ {self.id}: {self.bouquet}'