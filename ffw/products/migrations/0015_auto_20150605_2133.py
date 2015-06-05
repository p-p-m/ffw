# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20150605_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='subsubcategory',
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(related_name='products', default=1, verbose_name='Product subcategory', to='products.Subcategory'),
            preserve_default=False,
        ),
    ]
