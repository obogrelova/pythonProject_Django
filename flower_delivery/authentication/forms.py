from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}),
            'password1': forms.TextInput(attrs={'class': 'form-control', 'id': 'password1'}),
            'password2': forms.TextInput(attrs={'class': 'form-control', 'id': 'password2'}),
            }