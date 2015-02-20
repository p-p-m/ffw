# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20150210_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price_eur',
            field=models.DecimalField(null=True, verbose_name='Product price in EUR', max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='price_uah',
            field=models.DecimalField(null=True, verbose_name='Product price in UAH', max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='price_usd',
            field=models.DecimalField(null=True, verbose_name='Product price in USD', max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
