from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from cashback.services import generate_cashback
from products.models import Product

from .models import Order, OrderItem

CART_SESSION_KEY = 'cart'


def _get_cart(session):
    return session.get(CART_SESSION_KEY, {})


def _save_cart(session, cart):
    session[CART_SESSION_KEY] = cart
    session.modified = True


def _build_cart_items(cart):
    product_ids = [int(product_id) for product_id in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)
    products_by_id = {product.id: product for product in products}
    items = []
    total = Decimal('0')
    cashback_total = Decimal('0')

    for product_id, quantity in cart.items():
        product = products_by_id.get(int(product_id))
        if not product:
            continue

        subtotal = product.price * quantity
        item_cashback = (subtotal * product.cashback_percentage) / Decimal('100')
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
            'cashback_total': item_cashback,
        })
        total += subtotal
        cashback_total += item_cashback

    return items, total, cashback_total


def _require_buyer(user):
    return user.is_authenticated and user.role == 'buyer'


@login_required
def cart_detail(request):
    if not _require_buyer(request.user):
        return HttpResponseForbidden('Apenas compradores podem acessar o carrinho.')

    cart = _get_cart(request.session)
    items, total, cashback_total = _build_cart_items(cart)
    return render(request, 'orders/cart.html', {
        'cart_items': items,
        'cart_total': total,
        'cart_cashback_total': cashback_total,
    })


@login_required
def add_to_cart(request, product_id):
    if request.method != 'POST':
        return redirect('product_detail', pk=product_id)

    if not _require_buyer(request.user):
        return HttpResponseForbidden('Apenas compradores podem adicionar itens ao carrinho.')

    product = get_object_or_404(Product, pk=product_id)
    cart = _get_cart(request.session)
    product_key = str(product.id)
    cart[product_key] = cart.get(product_key, 0) + 1
    _save_cart(request.session, cart)
    messages.success(request, f'"{product.name}" foi adicionado ao carrinho.')
    return redirect('cart_detail')


@login_required
def update_cart_item(request, product_id):
    if request.method != 'POST':
        return redirect('cart_detail')

    if not _require_buyer(request.user):
        return HttpResponseForbidden('Apenas compradores podem atualizar o carrinho.')

    cart = _get_cart(request.session)
    product_key = str(product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity <= 0:
        cart.pop(product_key, None)
        messages.info(request, 'Item removido do carrinho.')
    else:
        cart[product_key] = quantity
        messages.success(request, 'Quantidade atualizada com sucesso.')

    _save_cart(request.session, cart)
    return redirect('cart_detail')


@login_required
def remove_from_cart(request, product_id):
    if request.method != 'POST':
        return redirect('cart_detail')

    if not _require_buyer(request.user):
        return HttpResponseForbidden('Apenas compradores podem remover itens do carrinho.')

    cart = _get_cart(request.session)
    cart.pop(str(product_id), None)
    _save_cart(request.session, cart)
    messages.info(request, 'Item removido do carrinho.')
    return redirect('cart_detail')


@login_required
def checkout(request):
    if request.method != 'POST':
        return redirect('cart_detail')

    if not _require_buyer(request.user):
        return HttpResponseForbidden('Apenas compradores podem finalizar compras.')

    cart = _get_cart(request.session)
    cart_items, total, _ = _build_cart_items(cart)

    if not cart_items:
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('cart_detail')

    order = Order.objects.create(user=request.user, total=total)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['product'].price,
        )

    generate_cashback(order)
    _save_cart(request.session, {})
    messages.success(request, 'Compra finalizada com sucesso. O cashback foi creditado na sua conta.')
    return redirect('cart_detail')
