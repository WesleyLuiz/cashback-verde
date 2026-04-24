from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cashback.models import Cashback
from products.models import Product

from .models import Order


class CartFlowTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.buyer = self.user_model.objects.create_user(
            username='buyer',
            password='test1234',
            role='buyer',
        )
        self.seller = self.user_model.objects.create_user(
            username='seller',
            password='test1234',
            role='seller',
        )
        self.product = Product.objects.create(
            seller=self.seller,
            name='Bicicleta urbana',
            description='Mobilidade sustentável.',
            price='1000.00',
            item_type=Product.TYPE_PRODUCT,
            category=Product.CATEGORY_SPORT,
            city=Product.CITY_JOAO_PESSOA,
            cashback_percentage='10.00',
            is_sustainable=True,
        )

    def test_buyer_can_add_item_to_cart(self):
        self.client.login(username='buyer', password='test1234')

        response = self.client.post(reverse('add_to_cart', args=[self.product.pk]))

        self.assertEqual(response.status_code, 302)
        session_cart = self.client.session.get('cart', {})
        self.assertEqual(session_cart[str(self.product.pk)], 1)

    def test_seller_cannot_access_cart(self):
        self.client.login(username='seller', password='test1234')

        response = self.client.get(reverse('cart_detail'))

        self.assertEqual(response.status_code, 403)

    def test_checkout_creates_order_and_generates_cashback(self):
        self.client.login(username='buyer', password='test1234')
        session = self.client.session
        session['cart'] = {str(self.product.pk): 2}
        session.save()

        response = self.client.post(reverse('checkout'))

        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(user=self.buyer)
        self.assertEqual(order.total, Decimal('2000.00'))
        self.assertEqual(order.orderitem_set.count(), 1)
        cashback = Cashback.objects.get(order=order)
        self.assertEqual(cashback.amount, Decimal('200.00'))

        self.buyer.refresh_from_db()
        self.assertEqual(self.buyer.cashback_balance, Decimal('200.00'))
