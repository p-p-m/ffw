# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_auto_20150208_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerimage',
            name='photo',
            field=models.ImageField(upload_to=b'static/gallery/', verbose_name='Foto'),
            preserve_default=True,
        ),
    ]
