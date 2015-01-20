# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from decimal import Decimal
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127, verbose_name='Category name')),
            ],
            options={
                'verbose_name': 'Category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=255, verbose_name='Product name')),
                ('code', models.CharField(unique=True, max_length=127, verbose_name='Product code')),
                ('price_uah', models.DecimalField(default=Decimal('0'), verbose_name='Product price in UAH', max_digits=8, decimal_places=2)),
                ('price_usd', models.DecimalField(default=Decimal('0'), verbose_name='Product price in USD', max_digits=8, decimal_places=2)),
                ('price_eur', models.DecimalField(default=Decimal('0'), verbose_name='Product price in EUR', max_digits=8, decimal_places=2)),
                ('short_description', models.CharField(help_text='This description will be shown on page with products list', max_length=1023, verbose_name='Product short description', blank=True)),
                ('description', models.TextField(verbose_name='Product description', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is product active')),
            ],
            options={
                'verbose_name': 'Product',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=63, verbose_name='Attribute name')),
                ('value', models.CharField(max_length=31, verbose_name='Attribute value')),
                ('product', models.ForeignKey(related_name='attributes', to='products.Product')),
            ],
            options={
                'verbose_name': 'Product attribute',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'products/', verbose_name='Image')),
                ('description', models.CharField(max_length=127, verbose_name='Image description')),
                ('product', models.ForeignKey(related_name='images', to='products.Product')),
            ],
            options={
                'verbose_name': 'Product image',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127, verbose_name='Subcategory name')),
                ('category', models.ForeignKey(related_name='subcategories', verbose_name='Category', to='products.Category')),
            ],
            options={
                'verbose_name': 'Subcategory',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(related_name='products', verbose_name='Product subcategory', to='products.Subcategory'),
            preserve_default=True,
        ),
    ]
