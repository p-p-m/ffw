# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import django.core.validators


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
                ('photo', core.models.ImageFieldWaterMark(upload_to=core.models.safe_upload, verbose_name=b'Photo')),
                ('link', models.URLField(default=b'', max_length=127, verbose_name='Link', blank=True, validators=[django.core.validators.URLValidator])),
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
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', core.models.ImageFieldWaterMark(upload_to=core.models.safe_upload, verbose_name=b'Photo')),
                ('link', models.URLField(default=b'', max_length=127, verbose_name='Link', blank=True, validators=[django.core.validators.URLValidator])),
                ('description', models.CharField(max_length=127, verbose_name='Image description', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is image active')),
            ],
            options={
                'verbose_name': 'Gallery Image',
                'verbose_name_plural': 'Gallery Images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GalleryPrimImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', core.models.ImageFieldWaterMark(upload_to=core.models.safe_upload, verbose_name=b'Photo')),
                ('link', models.URLField(default=b'', max_length=127, verbose_name='Link', validators=[django.core.validators.URLValidator])),
                ('description', models.CharField(max_length=255, verbose_name='Image description', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is image active')),
            ],
            options={
                'verbose_name': 'Gallery Primary Image ',
                'verbose_name_plural': 'Gallery Primary Images',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='gallery_prim_image',
            field=models.ForeignKey(related_name='images', to='gallery.GalleryPrimImage'),
            preserve_default=True,
        ),
    ]
