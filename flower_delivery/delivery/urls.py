from django.urls import path
from .views import cart_view, add_to_cart, update_cart, remove_from_cart, order_form_view

urlpatterns = [
    path('cart/', cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('order_form/', order_form_view, name='order_form'),
]