# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '__first__'),
        ('cart', '0001_initial'),
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
                ('contacts', models.CharField(max_length=255, verbose_name='Additional communication', blank=True)),
                ('total', models.DecimalField(verbose_name='Total', max_digits=9, decimal_places=2)),
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
                ('price', models.DecimalField(verbose_name='Price', max_digits=7, decimal_places=2)),
                ('quantity', models.IntegerField(verbose_name='Quantity')),
                ('sum', models.DecimalField(verbose_name='Sum', max_digits=9, decimal_places=2)),
                ('order', models.ForeignKey(related_name='products', verbose_name='Order', to='cart.Order')),
                ('product', models.ForeignKey(related_name='ordered_product', verbose_name='Product', to='products.Product')),
            ],
            options={
                'verbose_name': 'Ordered products',
                'verbose_name_plural': 'Ordered products',
            },
            bases=(models.Model,),
        ),
    ]
