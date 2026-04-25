from django.test import TestCase
from django.urls import reverse


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
