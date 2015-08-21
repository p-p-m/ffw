# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_auto_20150816_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default=datetime.datetime(2015, 8, 20, 11, 15, 27, 109000), max_length=125, verbose_name='Phone'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(default=0, verbose_name='Total', max_digits=9, decimal_places=2),
            preserve_default=True,
        ),
    ]
