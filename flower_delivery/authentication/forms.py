from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['user', 'email', 'password1', 'password2']
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}),
        }