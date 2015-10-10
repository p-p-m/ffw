# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20151003_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price_max',
            field=models.DecimalField(null=True, verbose_name='Max price in UAH', max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='price_min',
            field=models.DecimalField(null=True, verbose_name='Min price in UAH', max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
    ]
