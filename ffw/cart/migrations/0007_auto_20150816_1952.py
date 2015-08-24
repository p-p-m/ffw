# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_auto_20150816_1926'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='summ',
            new_name='total',
        ),
        migrations.RenameField(
            model_name='orderedproduct',
            old_name='summ',
            new_name='total',
        ),
    ]
