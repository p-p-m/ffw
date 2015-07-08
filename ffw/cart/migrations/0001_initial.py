# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(unique=True, max_length=127)),
                ('price_uah', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
