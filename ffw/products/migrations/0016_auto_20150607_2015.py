# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20150605_2133'),
    ]

    operations = [
        migrations.CreateModel(
            name='Characteristic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Characteristic name')),
                ('description', models.TextField(verbose_name='Characteristic description', blank=True)),
                ('default_value', models.CharField(max_length=127, verbose_name='Default value', blank=True)),
                ('units', models.CharField(max_length=50, verbose_name='Units', blank=True)),
            ],
            options={
                'verbose_name': 'Characteristic',
                'verbose_name_plural': 'Characteristics',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='category',
            name='characteristics',
            field=models.ManyToManyField(to='products.Characteristic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='section',
            name='characteristics',
            field=models.ManyToManyField(to='products.Characteristic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subcategory',
            name='characteristics',
            field=models.ManyToManyField(to='products.Characteristic'),
            preserve_default=True,
        ),
    ]
