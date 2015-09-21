# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import model_utils.fields
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127, verbose_name='Name')),
                ('slug', models.CharField(help_text='This field will be shown in URL address (for SEO). It will be filled automatically.', unique=True, max_length=127, verbose_name='Slug')),
                ('is_active', models.BooleanField(default=True)),
                ('image', core.models.ImageFieldWaterMark(upload_to=core.models.safe_upload, verbose_name='Image', blank=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryCharacteristic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(to='products.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Characteristic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Characteristic name')),
                ('description', models.TextField(verbose_name='Characteristic description', blank=True)),
                ('default_value', models.CharField(max_length=127, verbose_name='Default value', blank=True)),
                ('units', models.CharField(max_length=50, verbose_name='Units', blank=True)),
                ('rating', models.FloatField(default=4.0, help_text='Characteristic with higher ratings will be displayed first', verbose_name='Rating')),
                ('is_default', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Characteristic',
                'verbose_name_plural': 'Characteristics',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('positive_sides', models.TextField(verbose_name='Positive sides', blank=True)),
                ('negative_sides', models.TextField(verbose_name='Negative sides', blank=True)),
                ('is_approved', models.BooleanField(default=False, help_text='Only approved comments is visible for users', verbose_name='Is approved by stuff')),
            ],
            options={
                'verbose_name': 'Product comment',
                'verbose_name_plural': 'Product comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(help_text='This field will be shown in URL address (for SEO). It will be filled automatically.', unique=True, max_length=255, verbose_name='Slug')),
                ('short_description', models.CharField(help_text='This description will be shown on page with products list', max_length=1023, verbose_name='Product short description', blank=True)),
                ('description', models.TextField(verbose_name='Product description', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is product active')),
                ('rating', models.FloatField(default=4, help_text='Number between 0 and 5 that will be used for default sorting on products page. Products with higher numbers will be displayed higher', verbose_name='Product rating', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('price_min', models.DecimalField(null=True, verbose_name='Max price in UAH', max_digits=10, decimal_places=2)),
                ('price_max', models.DecimalField(null=True, verbose_name='Min price in UAH', max_digits=10, decimal_places=2)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=63, verbose_name='Name')),
                ('value', models.CharField(max_length=31, verbose_name='Value')),
                ('value_float', models.FloatField(help_text='This field will be defined automatically', null=True, verbose_name='Attribute value as number', blank=True)),
                ('units', models.CharField(max_length=50, verbose_name='Units', blank=True)),
                ('characteristic', models.ForeignKey(related_name='attributes', to='products.Characteristic', null=True)),
            ],
            options={
                'verbose_name': 'Product attribute',
                'verbose_name_plural': 'Product attributes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=127, verbose_name='Code')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('price_uah', models.DecimalField(null=True, verbose_name='Price in UAH', max_digits=10, decimal_places=2)),
                ('price_eur', models.DecimalField(null=True, verbose_name='Price in EUR', max_digits=10, decimal_places=2)),
                ('price_usd', models.DecimalField(null=True, verbose_name='Price in USD', max_digits=10, decimal_places=2)),
                ('product', models.ForeignKey(related_name='configurations', verbose_name='Product', to='products.Product')),
            ],
            options={
                'verbose_name': 'Product configuration',
                'verbose_name_plural': 'Product configurations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', core.models.ImageFieldWaterMark(upload_to=core.models.safe_upload, verbose_name='Image')),
                ('description', models.CharField(max_length=127, verbose_name='Image description', blank=True)),
                ('is_main', models.BooleanField(default=True, help_text='If image is main - it will be displayed on product list page')),
                ('product', models.ForeignKey(related_name='images', to='products.Product')),
            ],
            options={
                'verbose_name': 'Product image',
                'verbose_name_plural': 'Product images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127, verbose_name='Name')),
                ('slug', models.CharField(help_text='This field will be shown in URL address (for SEO). It will be filled automatically.', unique=True, max_length=127, verbose_name='Slug')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Section',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SectionCharacteristic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('characteristic', models.ForeignKey(to='products.Characteristic')),
                ('section', models.ForeignKey(to='products.Section')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127, verbose_name='Name')),
                ('slug', models.CharField(help_text='This field will be shown in URL address (for SEO). It will be filled automatically.', unique=True, max_length=127, verbose_name='Slug')),
                ('is_active', models.BooleanField(default=True)),
                ('image', core.models.ImageFieldWaterMark(upload_to=core.models.safe_upload, verbose_name='Image', blank=True)),
                ('is_on_main_page', models.BooleanField(default=True, verbose_name='Is on main page')),
                ('category', models.ForeignKey(related_name='subcategories', verbose_name='Category', to='products.Category')),
            ],
            options={
                'verbose_name': 'Subcategory',
                'verbose_name_plural': 'Subcategories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubcategoryCharacteristic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('characteristic', models.ForeignKey(to='products.Characteristic')),
                ('subcategory', models.ForeignKey(to='products.Subcategory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='characteristics',
            field=models.ManyToManyField(related_name='subcategories', through='products.SubcategoryCharacteristic', to='products.Characteristic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='section',
            name='characteristics',
            field=models.ManyToManyField(related_name='sections', through='products.SectionCharacteristic', to='products.Characteristic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='productattribute',
            name='product_configuration',
            field=models.ForeignKey(related_name='attributes', to='products.ProductConfiguration'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='materials',
            field=models.ForeignKey(verbose_name='Consumables and accessories', blank=True, to='products.Subcategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(related_name='products', verbose_name='Subcategory', to='products.Subcategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(related_name='comments', to='products.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categorycharacteristic',
            name='characteristic',
            field=models.ForeignKey(to='products.Characteristic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='characteristics',
            field=models.ManyToManyField(related_name='categories', through='products.CategoryCharacteristic', to='products.Characteristic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='section',
            field=models.ForeignKey(related_name='categories', verbose_name='Section', to='products.Section'),
            preserve_default=True,
        ),
    ]
