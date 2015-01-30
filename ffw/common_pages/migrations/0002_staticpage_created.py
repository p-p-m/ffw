# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('common_pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staticpage',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 29, 22, 47, 1, 919000), auto_now_add=True),
            preserve_default=False,
        ),
    ]
