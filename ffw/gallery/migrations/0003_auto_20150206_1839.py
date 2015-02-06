# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20150205_1951'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bannerimage',
            old_name='image',
            new_name='photo',
        ),
    ]
