# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20150220_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='value_float',
            field=models.FloatField(help_text='This field will be defined automatically', null=True, verbose_name='Attribute value as number', blank=True),
            preserve_default=True,
        ),
    ]
