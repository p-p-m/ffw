# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='productattribute',
            options={'verbose_name': 'Product attribute', 'verbose_name_plural': 'Product attributes'},
        ),
        migrations.AlterModelOptions(
            name='productimage',
            options={'verbose_name': 'Product image', 'verbose_name_plural': 'Product images'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name': 'Subcategory', 'verbose_name_plural': 'Subcategories'},
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(help_text='This field will be shown in product URL (for SEO). It will be filled automatically.', max_length=255, verbose_name='Product slug', blank=True),
            preserve_default=True,
        ),
    ]
