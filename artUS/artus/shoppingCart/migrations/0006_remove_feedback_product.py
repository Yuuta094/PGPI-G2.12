# Generated by Django 4.2.5 on 2023-12-03 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingCart', '0005_alter_order_total_price_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='product',
        ),
    ]