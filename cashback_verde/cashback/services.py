from .models import Cashback

def generate_cashback(order):
    percentage = 0.05  # 5%

    cashback_value = order.total * percentage

    Cashback.objects.create(
        user=order.user,
        order=order,
        amount=cashback_value
    )

    order.user.cashback_balance += cashback_value
    order.user.save()