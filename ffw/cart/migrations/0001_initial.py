# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('email', models.EmailField(max_length=125, verbose_name='E-mail')),
                ('phone', models.CharField(max_length=125, verbose_name='Phone')),
                ('contacts', models.CharField(max_length=255, verbose_name='Additional communication', blank=True)),
                ('total', models.DecimalField(default=0, verbose_name='Total', max_digits=9, decimal_places=2)),
                ('count', models.IntegerField(default=0, verbose_name='Quantity')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127, verbose_name='Name')),
                ('code', models.CharField(max_length=127, verbose_name='Code')),
                ('price', models.DecimalField(verbose_name='Price', max_digits=7, decimal_places=2)),
                ('quant', models.IntegerField(default=0, verbose_name='Quantity')),
                ('total', models.DecimalField(verbose_name='Total', max_digits=9, decimal_places=2)),
                ('order', models.ForeignKey(related_name='products', verbose_name='Order', to='cart.Order')),
                ('product', models.ForeignKey(related_name='ordered_product', verbose_name='Product', to='products.ProductConfiguration')),
            ],
            options={
                'verbose_name': 'Ordered products',
                'verbose_name_plural': 'Ordered products',
            },
            bases=(models.Model,),
        ),
    ]
