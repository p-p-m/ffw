# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common_pages', '0002_staticpage_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticpage',
            name='slug',
            field=models.SlugField(unique=True, max_length=250),
            preserve_default=True,
        ),
    ]
