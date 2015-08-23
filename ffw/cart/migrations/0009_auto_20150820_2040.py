# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_auto_20150820_1115'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='quant',
            new_name='count',
        ),
    ]
