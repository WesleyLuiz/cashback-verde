from django.db import models
from django.conf import settings


class Product(models.Model):
    TYPE_PRODUCT = 'product'
    TYPE_SERVICE = 'service'

    CATEGORY_SPORT = 'sport'
    CATEGORY_TOURISM = 'tourism'
    CATEGORY_HEALTH = 'health'
    CATEGORY_OTHER = 'other'

    CITY_JOAO_PESSOA = 'joao-pessoa'
    CITY_CABEDELO = 'cabedelo'

    ITEM_TYPE_CHOICES = [
        (TYPE_PRODUCT, 'Produto'),
        (TYPE_SERVICE, 'Serviço'),
    ]

    CATEGORY_CHOICES = [
        (CATEGORY_SPORT, 'Esporte'),
        (CATEGORY_TOURISM, 'Turismo'),
        (CATEGORY_HEALTH, 'Saúde'),
        (CATEGORY_OTHER, 'Outros'),
    ]

    CITY_CHOICES = [
        (CITY_JOAO_PESSOA, 'João Pessoa'),
        (CITY_CABEDELO, 'Cabedelo'),
    ]

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    city = models.CharField(max_length=20, choices=CITY_CHOICES)
    is_sustainable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
