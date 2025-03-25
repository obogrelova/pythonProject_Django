from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Product(models.Model):
    product = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    phone = models.CharField(max_length=30)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Заказ #{self.id} от {self.username}'