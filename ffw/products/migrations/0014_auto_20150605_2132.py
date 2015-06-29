# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20150319_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127, verbose_name='Section name')),
                ('slug', models.CharField(help_text='This field will be shown in URL address (for SEO). It will be filled automatically.', unique=True, max_length=127, verbose_name='Section slug')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Section',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='product',
            name='subcategory',
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to='products/', verbose_name='Image', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='section',
            field=models.ForeignKey(related_name='categories', default=1, verbose_name='Section', to='products.Section'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='subsubcategory',
            field=models.ForeignKey(related_name='products', default=1, verbose_name='Product subsubcategory', to='products.Subcategory'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=127, verbose_name='Subcategory name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='image',
            field=models.ImageField(upload_to='products/', verbose_name='Image', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='slug',
            field=models.CharField(help_text='This field will be shown in URL address (for SEO). It will be filled automatically.', unique=True, max_length=127, verbose_name='Subcategory slug'),
            preserve_default=True,
        ),
    ]
