from django.db import models

# Create your models here.

class Product(models.Model):
    bouquet = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.bouquet


class Order(models.Model):
    bouquet = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return f'Заказ {self.id}: {self.bouquet}'