from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Product


class ProductViewsTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.seller = self.user_model.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='test1234',
            role='seller',
        )
        self.other_seller = self.user_model.objects.create_user(
            username='other-seller',
            email='other-seller@example.com',
            password='test1234',
            role='seller',
        )
        self.buyer = self.user_model.objects.create_user(
            username='buyer',
            email='buyer@example.com',
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
            cashback_percentage='8.00',
        )
        self.service = Product.objects.create(
            seller=self.seller,
            name='Passeio ecológico',
            description='Serviço local para turismo sustentável.',
            price='250.00',
            item_type=Product.TYPE_SERVICE,
            category=Product.CATEGORY_TOURISM,
            city=Product.CITY_CABEDELO,
            cashback_percentage='12.00',
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
            'cashback_percentage': '10.00',
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

    def test_product_list_filters_by_multiple_categories(self):
        health_service = Product.objects.create(
            seller=self.seller,
            name='Yoga ao ar livre',
            description='Serviço de saúde e bem-estar.',
            price='80.00',
            item_type=Product.TYPE_SERVICE,
            category=Product.CATEGORY_HEALTH,
            city=Product.CITY_JOAO_PESSOA,
            cashback_percentage='10.00',
        )

        response = self.client.get(reverse('product_list'), {
            'item_type': Product.TYPE_SERVICE,
            'category': f'{Product.CATEGORY_TOURISM},{Product.CATEGORY_HEALTH}',
        })

        self.assertContains(response, 'Passeio ecológico')
        self.assertContains(response, health_service.name)
        self.assertNotContains(response, 'Bicicleta')

    def test_product_detail_shows_cashback_information(self):
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))

        self.assertContains(response, '8.00% cashback')
        self.assertContains(response, 'R$ 96.00')

    def test_seller_can_update_own_product(self):
        self.client.login(username='seller', password='test1234')

        response = self.client.post(reverse('product_update', args=[self.product.pk]), data={
            'name': 'Bicicleta revisada',
            'description': self.product.description,
            'price': self.product.price,
            'item_type': self.product.item_type,
            'category': self.product.category,
            'city': self.product.city,
            'cashback_percentage': self.product.cashback_percentage,
        })

        self.product.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.product.name, 'Bicicleta revisada')

    def test_buyer_cannot_update_product(self):
        self.client.login(username='buyer', password='test1234')

        response = self.client.get(reverse('product_update', args=[self.product.pk]))

        self.assertEqual(response.status_code, 403)

    def test_other_seller_cannot_update_product(self):
        self.client.login(username='other-seller', password='test1234')

        response = self.client.get(reverse('product_update', args=[self.product.pk]))

        self.assertEqual(response.status_code, 403)

    def test_seller_can_delete_own_product(self):
        self.client.login(username='seller', password='test1234')

        response = self.client.post(reverse('product_delete', args=[self.product.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_other_seller_cannot_delete_product(self):
        self.client.login(username='other-seller', password='test1234')

        response = self.client.post(reverse('product_delete', args=[self.product.pk]))

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())
