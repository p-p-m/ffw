# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common_pages', '0005_auto_20150131_2326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staticpageimage',
            name='image',
        ),
        migrations.AddField(
            model_name='staticpageimage',
            name='photo',
            field=models.ImageField(default=None, upload_to=b'common_pages/static/common_pages', verbose_name='Photo'),
            preserve_default=False,
        ),
    ]
