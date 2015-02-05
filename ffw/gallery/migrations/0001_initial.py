# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Banner name')),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banners',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BannerImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'static pages/', verbose_name='Image')),
                ('url_image', models.CharField(max_length=127, verbose_name='URL')),
                ('description', models.CharField(max_length=127, verbose_name='Image description', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is image active')),
                ('banner', models.ForeignKey(related_name='images', to='gallery.Banner')),
            ],
            options={
                'verbose_name': 'Banner Image',
                'verbose_name_plural': 'Banner Images',
            },
            bases=(models.Model,),
        ),
    ]
