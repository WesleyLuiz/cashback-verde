from .models import Cashback
from decimal import Decimal

def generate_cashback(order):
    cashback_value = sum(
        (
            (item.price * item.quantity * item.product.cashback_percentage) / Decimal('100')
            for item in order.orderitem_set.select_related('product')
        ),
        Decimal('0'),
    )

    if cashback_value <= 0:
        return

    Cashback.objects.create(
        user=order.user,
        order=order,
        amount=cashback_value
    )

    order.user.cashback_balance += cashback_value
    order.user.save()
