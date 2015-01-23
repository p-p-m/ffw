# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_slugs_are_unique'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price_eur',
            field=models.DecimalField(default=Decimal('0'), verbose_name='Product price in EUR', max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='price_uah',
            field=models.DecimalField(default=Decimal('0'), verbose_name='Product price in UAH', max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='price_usd',
            field=models.DecimalField(default=Decimal('0'), verbose_name='Product price in USD', max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
    ]
