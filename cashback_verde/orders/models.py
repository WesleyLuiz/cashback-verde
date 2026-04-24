from django.conf import settings
from django.db import models
from decimal import Decimal

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido #{self.pk}'

    def cashback_total(self):
        return sum(
            (item.cashback_total() for item in self.orderitem_set.select_related('product')),
            Decimal('0'),
        )

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'

    def subtotal(self):
        return self.price * self.quantity

    def cashback_total(self):
        return (self.subtotal() * self.product.cashback_percentage) / Decimal('100')
