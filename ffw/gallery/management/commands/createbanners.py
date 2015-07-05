# coding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from gallery import models


class Command(BaseCommand):
    args = 'no args for this command'
    help = 'Creates top and main banners'

    def handle(self, *args, **options):
        models.Banner.objects.get_or_create(name='main')
