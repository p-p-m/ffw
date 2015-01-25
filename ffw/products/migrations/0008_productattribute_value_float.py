# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20150125_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattribute',
            name='value_float',
            field=models.FloatField(help_text='This field will be defined automatically', null=True, verbose_name='Attribute value as number'),
            preserve_default=True,
        ),
    ]
