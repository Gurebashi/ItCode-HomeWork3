# Generated by Django 5.1.2 on 2024-10-28 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_cart_cartitem_order_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='quantity',
        ),
    ]