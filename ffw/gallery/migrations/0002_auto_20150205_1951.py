# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerimage',
            name='image',
            field=models.ImageField(upload_to=b'banner_images/', verbose_name='Image'),
            preserve_default=True,
        ),
    ]
