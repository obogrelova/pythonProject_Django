from django import forms
from .models import Product, Order

class ProductForm(forms.ModelForm):
    flowers = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-input'}))
    price = forms.DecimalField(label='Цена', widget=forms.TextInput(attrs={'class': 'form-input'}))
    image = forms.ImageField(label='Изображение', widget=forms.ClearableFileInput(attrs={'class': 'form-control-lg'}))

    class Meta:
        model = Product
        fields = ['flowers', 'price', 'image']


class OrderForm(forms.ModelForm):
    username = forms.CharField(label='Имя клиента', widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-input'}))
    flowers = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Order
        fields = ['username', 'phone', 'flowers']