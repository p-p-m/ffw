# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20150206_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerimage',
            name='photo',
            field=models.ImageField(upload_to=b'galerry/static/gallery/', verbose_name='Foto'),
            preserve_default=True,
        ),
    ]
