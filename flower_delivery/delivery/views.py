from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .telegram_bot.bot import send_message

# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'delivery/home.html', {'products': products})

def place_order(request):
    if request.method == 'POST':
        bouquet = request.POST.get('bouquet')
        user = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')


        order = Order.objects.create(bouquet=bouquet, user=user, phone=phone, email=email, address=address)

        text = f'Новый заказ!\nБукет: {order.bouquet}\nКлиент: {order.user}\nТелефон: {order.phone}\nПочта: {order.email}\nАдрес: {order.address}'
        send_message(text)

        return redirect('success_page')
    return render(request, 'order_form.html')

@login_required
def cart_view(request):
    cart_items = Order.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'delivery/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Order.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'Добавлено в корзину: {product.name}')
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