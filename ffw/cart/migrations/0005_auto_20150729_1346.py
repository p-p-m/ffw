# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_auto_20150728_0952'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='sum',
            new_name='summ',
        ),
        migrations.RenameField(
            model_name='orderedproduct',
            old_name='sum',
            new_name='summ',
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='code',
            field=models.CharField(default=datetime.datetime(2015, 7, 29, 13, 45, 17, 328000), unique=True, max_length=127, verbose_name='Code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='name',
            field=models.CharField(default=datetime.datetime(2015, 7, 29, 13, 46, 33, 671000), max_length=127, verbose_name='Name'),
            preserve_default=False,
        ),
    ]
