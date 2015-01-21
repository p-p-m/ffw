# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_add_slug_field_and_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.CharField(default='slug', help_text='This field will be shown in URL address (for SEO). It will be filled automatically.', max_length=127, verbose_name='Category slug'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subcategory',
            name='slug',
            field=models.CharField(default='slug', help_text='This field will be shown in URL address (for SEO). It will be filled automatically.', max_length=127, verbose_name='Category slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(help_text='This field will be shown in URL address (for SEO). It will be filled automatically.', max_length=255, verbose_name='Product slug'),
            preserve_default=True,
        ),
    ]
