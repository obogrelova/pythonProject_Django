from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from delivery.telegram_bot.bot import send_message
from django.http import JsonResponse
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
            order.user = request.user
            order.save()

            text = f'Новый заказ!\nБукет: {order.product}\nКлиент: {order.user}\nТелефон: {order.phone}'
            send_message(text)

            return redirect('home')
    else:
        form =OrderForm()
    return render(request, 'delivery/order_form.html', {'form': form})

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            cart_items.append({'product': product, 'quantity': quantity, 'total_price': product.price * quantity})
            total += product.price * quantity
        except Product.DoesNotExist:
            pass
    return render(request, 'delivery/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        print(f'Получен запрос на добавление: Продукт ID={product_id}, Количество={quantity}')

        cart_item, created = Order.objects.get_or_create(user=request.user, product=product)

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

        print(f'Обновлено: Продукт ID={product_id}, Количество в корзине={cart_item.quantity}')

        cart_count = Order.objects.filter(user=request.user).count()
        return JsonResponse({'cart_count': cart_count})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


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
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(Order, user=request.user, product_id=product_id)
    cart_item.delete()
    messages.success(request, 'Товар удален из корзины.')
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