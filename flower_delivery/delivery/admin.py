from django.contrib import admin
from .models import Product, Order

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('bouquet', 'price', 'image')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('bouquet', 'user', 'phone', 'email', 'address')
