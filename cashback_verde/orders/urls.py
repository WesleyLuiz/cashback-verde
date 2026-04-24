from django.urls import path

from .views import add_to_cart, cart_detail, checkout, remove_from_cart, update_cart_item

urlpatterns = [
    path('carrinho/', cart_detail, name='cart_detail'),
    path('carrinho/adicionar/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('carrinho/atualizar/<int:product_id>/', update_cart_item, name='update_cart_item'),
    path('carrinho/remover/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('carrinho/finalizar/', checkout, name='checkout'),
]
