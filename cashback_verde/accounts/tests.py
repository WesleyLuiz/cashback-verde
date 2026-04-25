from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import CustomUserCreationForm


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
