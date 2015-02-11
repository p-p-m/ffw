# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0007_auto_20150210_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerimage',
            name='photo',
            field=models.ImageField(upload_to=b'gallery/static/gallery', verbose_name='Photo'),
            preserve_default=True,
        ),
    ]
