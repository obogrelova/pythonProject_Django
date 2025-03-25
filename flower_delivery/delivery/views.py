from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from delivery.telegram_bot.bot import send_message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from delivery.telegram_bot.bot import send_message
from delivery.telegram_bot.config import TELEGRAM_BOT_TOKEN, ADMIN_CHAT_ID


# Create your views here.

def send_telegram_message_sync(message: str):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': ADMIN_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        print(f'Сообщение успешно отправлено: {response.json()}')
    except requests.RequestException as e:
        print(f'Ошибка отправки сообщения в Telegram: {e}')


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
            return redirect('home')
    else:
        form =OrderForm()
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
    return render(request, '/delivery/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity
    })


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
def remove_from_cart(request, product_id):
    cart = request.session.get('cart_view', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart_view'] = cart
    return redirect('cart_view')


@login_required
def order_form_view(request):
    cart = request.session.get('cart_view', {})

    if not cart:
        return redirect('cart_view')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user

            cart_item = []
            total_price = 0

            for product_id, quantity in cart.items():
                product = Product.objects.get(id=int(product_id))
                item_total = product.price * quantity
                total_price += item_total
                cart_item.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': item_total
                })

            order.total_price = total_price
            order.save()

            message = f'Новый заказ #{order.id}\n\n'
            message += f'Имя клиента: {order.username}\n'
            message += f'Телефон: {order.phone}\n'
            message += '\nПродукт:\n'

            for item in cart_items:
                message += f"- {item['product'].product} × {item['total_price']}₽\n"

            message += f'\nОбщая сумма: {total_price}₽'
            message += f"\nДата заказа: {order.created_at.strftime('%d.%m.%Y %H:%M')}"

            send_telegram_message_sync(message)

            request.session['cart_view'] = {}
            messages.success(request, 'Заказ успешно оформлен!')
            return redirect('order_success', order_id=order.id)


def order_success(request, order_id):
    return render(request, '/delivery/success_page.html', {'order_id': order_id})


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

    message.success(request, f'{product.product} добавлен в корзину')
    return redirect('cart_view')


@csrf_exempt
def update_cart(request, product_id):
    if request.mathod == 'POST':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))

            cart = request.session.get('cart_view', {})
            cart[str(product_id)] = quantity
            request.session['cart_view'] = cart
            request.session.modified = True

            total_price = sum(
                Product.objects.get(id=int(product_id)).price * quantity
                for product_id, quantity in cart.items()
            )
            total_quantity = sum(cart.values())

            return JsonResponse({
                'success': True,
                'total_quantity': total_quantity,
                'total_price': total_price
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)