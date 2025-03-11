from django.db import models

# Create your models here.

class User(models.Model):
    user = models.CharField('Имя клиента', max_length=255)
    email = models.EmailField('Электронная почта', unique=True)

    def __str__(self):
        return self.user
