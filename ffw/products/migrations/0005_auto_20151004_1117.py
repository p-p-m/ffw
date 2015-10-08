# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20151004_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comments',
            field=models.TextField(verbose_name='Comments', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='username',
            field=models.CharField(default='undefined', max_length=128),
            preserve_default=False,
        ),
    ]
