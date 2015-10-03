# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_characteristic_is_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='productconfiguration',
            name='article',
            field=models.CharField(max_length=127, verbose_name='Article', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='productconfiguration',
            name='code',
            field=models.CharField(max_length=127, verbose_name='Code'),
            preserve_default=True,
        ),
    ]
