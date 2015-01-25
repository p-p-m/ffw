# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attribute_name', models.CharField(max_length=63, verbose_name='Attribute name')),
                ('name', models.CharField(max_length=63, verbose_name='Filter displayed name')),
                ('filter_type', models.CharField(max_length=15, choices=[('NUMERIC', 'Numeric filter'), ('CHOICES', 'Choices filter'), ('NUMERIC_RANGES', 'Intervals filter')])),
                ('ranges_count', models.SmallIntegerField(default=5, help_text='This field is necessary only for interval filters', null=True, verbose_name='Amount of ranges', validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(50)])),
                ('values', jsonfield.fields.JSONField(default={}, help_text='Internal filter values. DO NOT modify them.', verbose_name='Filter values')),
                ('category', models.ForeignKey(related_name='product_filters', to='products.Category', null=True)),
                ('subcategory', models.ForeignKey(related_name='product_filters', to='products.Subcategory', null=True)),
            ],
            options={
                'verbose_name': 'Product filter',
                'verbose_name_plural': 'Product filters',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='image',
            field=models.ImageField(default='image.png', upload_to='products/', verbose_name='Image'),
            preserve_default=False,
        ),
    ]
