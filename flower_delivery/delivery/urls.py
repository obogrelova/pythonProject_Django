from django.urls import path
from . import views
from .views import home, cart_view, add_to_cart, remove_from_cart, update_cart, order_form_view, order_success

urlpatterns = [
    path('', home, name='home'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', update_cart, name='update_cart'),
    path('order_form/', order_form_view, name='order_form'),
    path('order-success/<int:order_id>/', order_success, name='order_success'),
    path('order/', views.place_order, name='place_order'),
]