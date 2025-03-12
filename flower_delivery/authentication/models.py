from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(verbose_name='Имя клиента', max_length=255)
    email = models.EmailField(verbose_name='Электронная почта', unique=True)

    def __str__(self):
        return self.username
