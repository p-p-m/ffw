# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_auto_20150820_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderedproduct',
            name='code',
            field=models.CharField(max_length=127, verbose_name='Code'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderedproduct',
            name='total',
            field=models.DecimalField(verbose_name='Total', max_digits=9, decimal_places=2),
            preserve_default=True,
        ),
    ]
