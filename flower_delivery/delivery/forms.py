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
        fields = ['bouquet', 'name', 'phone', 'email', 'address']
        widgets = {
            'bouquet': forms.TextInput(attrs={'class': 'form-control', 'id': 'bouquet'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'id': 'address'}),
        }