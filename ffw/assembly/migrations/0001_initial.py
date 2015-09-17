# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChoicesAttributeFilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('priority', models.FloatField(default=1, help_text='Filters with higher priority are displayed higher on page', verbose_name='Priority')),
                ('is_auto_update', models.BooleanField(default=True, help_text='If auto update is activated - filter will be automatically fill his fields.')),
                ('choices', models.TextField(help_text='Comma-separated list of choices', verbose_name='Choices', blank=True)),
                ('category', models.ForeignKey(to='products.Category', null=True)),
                ('characteristic', models.ForeignKey(to='products.Characteristic')),
                ('section', models.ForeignKey(to='products.Section', null=True)),
                ('subcategory', models.ForeignKey(to='products.Subcategory', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IntervalsAttributeFilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('priority', models.FloatField(default=1, help_text='Filters with higher priority are displayed higher on page', verbose_name='Priority')),
                ('is_auto_update', models.BooleanField(default=True, help_text='If auto update is activated - filter will be automatically fill his fields.')),
                ('intervals', models.TextField(help_text='Comma-separated list of intervals. Example: 0-100, 100-200 ...', verbose_name='Intervals', blank=True)),
                ('category', models.ForeignKey(to='products.Category', null=True)),
                ('characteristic', models.ForeignKey(to='products.Characteristic')),
                ('section', models.ForeignKey(to='products.Section', null=True)),
                ('subcategory', models.ForeignKey(to='products.Subcategory', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NumericAttributeFilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('priority', models.FloatField(default=1, help_text='Filters with higher priority are displayed higher on page', verbose_name='Priority')),
                ('is_auto_update', models.BooleanField(default=True, help_text='If auto update is activated - filter will be automatically fill his fields.')),
                ('max_value', models.FloatField(default=0, verbose_name='Max')),
                ('min_value', models.FloatField(default=0, verbose_name='Min')),
                ('category', models.ForeignKey(to='products.Category', null=True)),
                ('characteristic', models.ForeignKey(to='products.Characteristic')),
                ('section', models.ForeignKey(to='products.Section', null=True)),
                ('subcategory', models.ForeignKey(to='products.Subcategory', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NumericPriceFilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('priority', models.FloatField(default=1, help_text='Filters with higher priority are displayed higher on page', verbose_name='Priority')),
                ('is_auto_update', models.BooleanField(default=True, help_text='If auto update is activated - filter will be automatically fill his fields.')),
                ('max_value', models.FloatField(default=0, verbose_name='Max')),
                ('min_value', models.FloatField(default=0, verbose_name='Min')),
                ('category', models.ForeignKey(to='products.Category', null=True)),
                ('section', models.ForeignKey(to='products.Section', null=True)),
                ('subcategory', models.ForeignKey(to='products.Subcategory', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
