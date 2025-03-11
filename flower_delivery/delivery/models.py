from django.db import models

# Create your models here.

class Product(models.Model):
    bouquet = models.CharField('Букет', max_length=255)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.bouquet


class Order(models.Model):
    bouquet = models.CharField('Букет', max_length=255)
    user = models.CharField('Имя клиента', max_length=255)
    phone = models.CharField('Телефон клиента', max_length=20)
    email = models.EmailField('Электронная почта', unique=True)
    address = models.TextField()

    def __str__(self):
        return f'Заказ {self.id}: {self.bouquet}'