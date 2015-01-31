# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common_pages', '0004_staticpageimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='staticpage',
            options={'verbose_name': 'StaticPage', 'verbose_name_plural': 'StaticPages'},
        ),
        migrations.AlterModelOptions(
            name='staticpageimage',
            options={'verbose_name': 'StaticPage Image', 'verbose_name_plural': 'StaticPage Images'},
        ),
        migrations.RenameField(
            model_name='staticpageimage',
            old_name='staticPage',
            new_name='staticpage',
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='StaticPage is active'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='slug',
            field=models.SlugField(unique=True, max_length=250, verbose_name='StaticPage slug'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='text',
            field=models.TextField(verbose_name='StaticPage text'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='title',
            field=models.CharField(max_length=250, verbose_name='StaticPage name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='staticpageimage',
            name='description',
            field=models.CharField(max_length=127, verbose_name='Image description', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='staticpageimage',
            name='image',
            field=models.ImageField(upload_to=b'static pages/', verbose_name='Image'),
            preserve_default=True,
        ),
    ]
