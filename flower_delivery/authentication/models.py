from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(verbose_name='Имя клиента', max_length=255)

    def __str__(self):
        return self.name