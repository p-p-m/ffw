# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_delete_testproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total',
        ),
        migrations.RemoveField(
            model_name='orderedproduct',
            name='quantity',
        ),
        migrations.AddField(
            model_name='order',
            name='quant',
            field=models.IntegerField(default=0, verbose_name='Quantity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='sum',
            field=models.DecimalField(default=0, verbose_name='Sum', max_digits=9, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='quant',
            field=models.IntegerField(default=0, verbose_name='Quantity'),
            preserve_default=True,
        ),
    ]
