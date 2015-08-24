# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_auto_20150729_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderedproduct',
            name='product',
            field=models.ForeignKey(related_name='ordered_product', verbose_name='Product', to='products.ProductConfiguration'),
            preserve_default=True,
        ),
    ]
