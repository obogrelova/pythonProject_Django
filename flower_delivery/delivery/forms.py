from django import forms
from .models import Product, Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['bouquet', 'price']
        widgets = {
            'bouquet': forms.TextInput(attrs={'class': 'form-control', 'id': 'bouquet'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'id': 'price'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['bouquet', 'username', 'phone']
        widgets = {
            'bouquet': forms.TextInput(attrs={'class': 'form-control', 'id': 'bouquet'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'username'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'phone'}),
        }