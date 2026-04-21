from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Product


class ProductViewsTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.seller = self.user_model.objects.create_user(
            username='seller',
            password='test1234',
            role='seller',
        )
        self.buyer = self.user_model.objects.create_user(
            username='buyer',
            password='test1234',
            role='buyer',
        )
        self.product = Product.objects.create(
            seller=self.seller,
            name='Bicicleta',
            description='Produto para mobilidade urbana.',
            price='1200.00',
            item_type=Product.TYPE_PRODUCT,
            category=Product.CATEGORY_SPORT,
            city=Product.CITY_JOAO_PESSOA,
            is_sustainable=True,
        )
        self.service = Product.objects.create(
            seller=self.seller,
            name='Passeio ecológico',
            description='Serviço local para turismo sustentável.',
            price='250.00',
            item_type=Product.TYPE_SERVICE,
            category=Product.CATEGORY_TOURISM,
            city=Product.CITY_CABEDELO,
            is_sustainable=True,
        )

    def test_only_seller_can_create_product(self):
        self.client.login(username='buyer', password='test1234')

        response = self.client.get(reverse('product_create'))

        self.assertEqual(response.status_code, 403)

    def test_seller_can_create_product_with_required_fields(self):
        self.client.login(username='seller', password='test1234')

        response = self.client.post(reverse('product_create'), data={
            'name': 'Consultoria esportiva',
            'description': 'Aulas de condicionamento.',
            'price': '99.90',
            'item_type': Product.TYPE_SERVICE,
            'category': Product.CATEGORY_SPORT,
            'city': Product.CITY_JOAO_PESSOA,
            'is_sustainable': 'on',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name='Consultoria esportiva').exists())

    def test_product_list_filters_by_item_type_category_and_city(self):
        response = self.client.get(reverse('product_list'), {
            'item_type': Product.TYPE_SERVICE,
            'category': Product.CATEGORY_TOURISM,
            'city': Product.CITY_CABEDELO,
        })

        self.assertContains(response, 'Passeio ecológico')
        self.assertNotContains(response, 'Bicicleta')
