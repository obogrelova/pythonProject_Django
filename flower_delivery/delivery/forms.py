from django import forms
from .models import Product, Order

class ProductForm(forms.ModelForm):
    name = forms.CharField(label='Букет', widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(label='Цена', widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label='Изображение', widget=forms.ClearableFileInput(attrs={'class': 'form-control-lg'}))

    class Meta:
        model = Product
        fields = ['name', 'price', 'image']


class OrderForm(forms.ModelForm):
    username = forms.CharField(label='Имя клиента', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['username', 'phone']