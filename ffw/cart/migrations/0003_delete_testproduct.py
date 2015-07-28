# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_order_orderedproduct'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TestProduct',
        ),
    ]
