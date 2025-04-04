from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import requests
from django.contrib import messages
from delivery.telegram_bot.message_to_admin import send_photo

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
    cart = request.session.get('cart_view', {})

    cart_items = []
    total_price = 0
    total_quantity = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=int(product_id))
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })
        total_price += product.price * quantity
        total_quantity += quantity

    return render(request, 'delivery/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart = request.session.get('cart_view', {})

    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity
    request.session['cart_view'] = cart
    request.session.modified = True

    messages.success(request, f'{product.name} добавлен в корзину')
    return redirect('cart_view')


@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart_view', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart_view'] = cart
    return redirect('cart_view')


@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        cart = request.session.get('cart_view', {})
        cart[str(product_id)] = quantity
        request.session['cart_view'] = cart
        request.session.modified = True

        total_price = sum(
            Product.objects.get(id=int(product_id)).price * quantity
            for product_id, quantity in cart.items()
        )
        total_quantity = sum(cart.values())

        return render(request, 'delivery/cart.html', {
            'success': True,
            'total_quantity': total_quantity,
            'total_price': total_price
        })


@login_required
def order_form_view(request):
    cart = request.session.get('cart_view', {})

    if not cart:
        return redirect('cart_view')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user

                cart_items = []
                total_price = 0

                for product_id, quantity in cart.items():
                    product = Product.objects.get(id=int(product_id))
                    item_total = product.price * quantity
                    total_price += item_total
                    cart_items.append({
                        'product': product,
                        'quantity': quantity,
                        'total_price': item_total
                    })

                    order.total_price = total_price
                    print(f'Сумма перед сохранением заказа: {total_price}')
                    order.save()

                    caption = (f'Новый заказ!\n'
                                f'Клиент: {order.username}\n'
                                f'Телефон: {order.phone}\n'
                                f'{product.name} - {quantity} шт.\n'
                                f'Цена: {total_price} ₽'
                    )
                    photo_path = os.path.join(settings.MEDIA_ROOT, product.image.name)
                    send_photo(photo_path, caption)

                request.session['cart_view'] = {}
                messages.success(request, 'Заказ успешно оформлен!')
                return redirect('order_success', order_id=order.id)
    else:
        form = OrderForm()

    cart_items = [
        {
            'product': Product.objects.get(id=int(product_id)),
            'quantity': quantity,
            'total_price': Product.objects.get(id=int(product_id)).price * quantity,
        }
        for product_id, quantity in cart.items()
    ]

    total = sum(item['total_price'] for item in cart_items)

    return render(request, 'delivery/order_form.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total
    })


def order_success(request, order_id):
    return render(request, 'delivery/success_page.html', {'order_id': order_id})