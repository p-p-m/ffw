# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_category_and_subcategory_slugs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(help_text='This field will be shown in URL address (for SEO). It will be filled automatically.', unique=True, max_length=127, verbose_name='Category slug'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(help_text='This field will be shown in URL address (for SEO). It will be filled automatically.', unique=True, max_length=255, verbose_name='Product slug'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='slug',
            field=models.CharField(help_text='This field will be shown in URL address (for SEO). It will be filled automatically.', unique=True, max_length=127, verbose_name='Category slug'),
            preserve_default=True,
        ),
    ]
