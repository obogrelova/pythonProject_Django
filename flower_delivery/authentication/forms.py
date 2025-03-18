from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'phone', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'username'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}),
        }