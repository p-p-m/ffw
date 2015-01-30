# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common_pages', '0003_auto_20150130_1810'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticPageImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'staticPage/', verbose_name=b'Image')),
                ('description', models.CharField(max_length=127, verbose_name=b'Image description')),
                ('staticPage', models.ForeignKey(related_name='images', to='common_pages.StaticPage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
