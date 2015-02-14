# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20150214_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerimage',
            name='link',
            field=models.URLField(default=b'', max_length=127, verbose_name='Link', blank=True, validators=[django.core.validators.URLValidator]),
            preserve_default=True,
        ),
    ]
