# Generated manually because Django is not available in the current environment.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_cashback_percentage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_sustainable',
        ),
    ]
