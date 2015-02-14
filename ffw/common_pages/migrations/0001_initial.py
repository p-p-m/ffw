# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250, verbose_name='StaticPage name')),
                ('slug', models.SlugField(unique=True, max_length=250, verbose_name='StaticPage slug')),
                ('text', models.TextField(verbose_name='StaticPage text')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('is_active', models.BooleanField(default=True, verbose_name='StaticPage is active')),
            ],
            options={
                'verbose_name': 'StaticPage',
                'verbose_name_plural': 'StaticPages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StaticPageImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(upload_to=b'common_pages/static/common_pages', verbose_name='Photo')),
                ('description', models.CharField(max_length=127, verbose_name='Image description', blank=True)),
                ('staticpage', models.ForeignKey(related_name='images', to='common_pages.StaticPage')),
            ],
            options={
                'verbose_name': 'StaticPage Image',
                'verbose_name_plural': 'StaticPage Images',
            },
            bases=(models.Model,),
        ),
    ]
