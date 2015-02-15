# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20150130_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='description',
            field=models.CharField(max_length=127, verbose_name='Image description', blank=True),
            preserve_default=True,
        ),
    ]
