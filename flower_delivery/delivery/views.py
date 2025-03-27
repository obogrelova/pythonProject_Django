from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from delivery.telegram_bot.bot import send_message
from delivery.telegram_bot.config import TELEGRAM_BOT_TOKEN, ADMIN_CHAT_ID
import requests


# Create your views here.


def home(request):
    products = Product.objects.all()
    return render(request, 'delivery/home.html', {'products': products})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
                order.save()
            return redirect('home')
    else:
        form = OrderForm()
    return render(request, 'delivery/order_form.html', {'form': form})


@login_required
def cart_view(request):
    cart_items = Order.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'delivery/cart.html', { 'cart_items': cart_items, 'total_price': total_price})



@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        if request.user.is_authenticated:
            user = request.user
            cart_item, created = Order.objects.get_or_create(user=user, complete=False)
            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()
        messages.success(request, f'{product.name} добавлен в корзину')
        return redirect('cart_view')


@login_required
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(Order, user=request.user, product_id=product_id)
    cart_item.delete()
    messages.success(request, 'Товар удален из корзины.')
    return redirect('cart_view')


@login_required
def update_cart(request, product_id):
    cart_item = get_object_or_404(Order, user=request.user, product_id=product_id)
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart_view')


@login_required
def order_form_view(request):
    cart_items = Order.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        cart_items.delete()
        messages.success(request, 'Заказ успешно оформлен!')
        return redirect('cart_view')

    return render(request, 'delivery/order_form.html', {'cart_items': cart_items, 'total_price': total_price})


def order_success(request, order_id):
    return render(request, 'delivery/success_page.html', {'order_id': order_id})