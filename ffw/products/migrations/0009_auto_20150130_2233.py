# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_productattribute_value_float'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfilter',
            name='category',
            field=models.ForeignKey(related_name='product_filters', blank=True, to='products.Category', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='productfilter',
            name='subcategory',
            field=models.ForeignKey(related_name='product_filters', blank=True, to='products.Subcategory', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='productfilter',
            name='values',
            field=jsonfield.fields.JSONField(default={}, help_text='Internal filter values. DO NOT modify them.', verbose_name='Filter values', blank=True),
            preserve_default=True,
        ),
    ]
