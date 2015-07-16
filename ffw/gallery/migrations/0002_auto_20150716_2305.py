# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerimage',
            name='photo',
            field=core.models.ImageFieldWaterMark(upload_to=b'gallery', verbose_name=b'Photo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='galleryimage',
            name='photo',
            field=core.models.ImageFieldWaterMark(upload_to=b'gallery/gallery', verbose_name=b'Photo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='galleryprimimage',
            name='photo',
            field=core.models.ImageFieldWaterMark(upload_to=b'gallery/gallery', verbose_name=b'Photo'),
            preserve_default=True,
        ),
    ]
