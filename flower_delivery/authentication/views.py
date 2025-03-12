from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import RegisterForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.save()
            login(request, username)
            return redirect('home')
        else:
            form = RegisterForm()

        return render(request, 'authentication/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'