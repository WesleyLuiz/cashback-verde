from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    BUYER = 'buyer'
    SELLER = 'seller'

    ROLE_CHOICES = [
        (BUYER, 'Comprador'),
        (SELLER, 'Vendedor'),
    ]

    email = models.EmailField('e-mail', unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=BUYER)
    cashback_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def is_buyer(self):
        return self.role == self.BUYER

    def is_seller(self):
        return self.role == self.SELLER
