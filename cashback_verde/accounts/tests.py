from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import CustomUserCreationForm
from products.models import Product


class AuthenticationViewsTests(TestCase):
    def test_login_page_uses_portuguese_labels_and_bootstrap_inputs(self):
        response = self.client.get(reverse('login'))

        self.assertContains(response, 'Nome de usuário')
        self.assertContains(response, 'Senha')
        self.assertContains(response, 'form-control form-control-lg')

    def test_register_page_uses_portuguese_labels_and_bootstrap_inputs(self):
        response = self.client.get(reverse('register'))

        self.assertContains(response, 'Nome de usuário')
        self.assertContains(response, 'E-mail')
        self.assertContains(response, 'Perfil')
        self.assertContains(response, 'form-control form-control-lg')
        self.assertContains(response, 'form-select form-select-lg')

    def test_seller_profile_lists_only_own_products(self):
        user_model = get_user_model()
        seller = user_model.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='test1234',
            role='seller',
        )
        other_seller = user_model.objects.create_user(
            username='other-seller',
            email='other-seller@example.com',
            password='test1234',
            role='seller',
        )
        own_product = Product.objects.create(
            seller=seller,
            name='Bicicleta',
            description='Produto para mobilidade urbana.',
            price='1200.00',
            item_type=Product.TYPE_PRODUCT,
            category=Product.CATEGORY_SPORT,
            city=Product.CITY_JOAO_PESSOA,
            cashback_percentage='8.00',
        )
        Product.objects.create(
            seller=other_seller,
            name='Passeio ecológico',
            description='Serviço local para turismo sustentável.',
            price='250.00',
            item_type=Product.TYPE_SERVICE,
            category=Product.CATEGORY_TOURISM,
            city=Product.CITY_CABEDELO,
            cashback_percentage='12.00',
        )
        self.client.login(username='seller', password='test1234')

        response = self.client.get(reverse('profile'))

        self.assertContains(response, 'Perfil: Vendedor')
        self.assertContains(response, own_product.name)
        self.assertContains(response, reverse('product_update', args=[own_product.pk]))
        self.assertNotContains(response, 'Passeio ecológico')


class CustomUserCreationFormTests(TestCase):
    def test_username_must_be_unique_with_portuguese_message(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username='usuario_existente',
            email='existente@example.com',
            password='test1234',
        )

        form = CustomUserCreationForm(data={
            'username': 'usuario_existente',
            'email': 'novo@example.com',
            'role': 'buyer',
            'password1': 'senha-forte-123',
            'password2': 'senha-forte-123',
        })

        self.assertFalse(form.is_valid())
        self.assertIn(
            'Já existe uma conta com este nome de usuário.',
            form.errors['username'],
        )

    def test_email_must_be_unique(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username='usuario_existente',
            email='teste@example.com',
            password='test1234',
        )

        form = CustomUserCreationForm(data={
            'username': 'novo_usuario',
            'email': 'TESTE@example.com',
            'role': 'buyer',
            'password1': 'senha-forte-123',
            'password2': 'senha-forte-123',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('Já existe uma conta cadastrada com este e-mail.', form.errors['email'])
