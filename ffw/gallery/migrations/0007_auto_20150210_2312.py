# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def bann_obj_create(apps, shema_editor):
    Banner = apps.get_model('gallery','Banner')
    b = Banner(name = 'top')
    b.save()
    b = Banner(name = 'main')
    b.save()
     

class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_auto_20150208_1351'),
    ]

    operations = [
        migrations.RunPython(bann_obj_create),
    ]
