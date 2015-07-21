# coding: utf-8
from __future__ import unicode_literals

import os

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from gallery import models


class Command(BaseCommand):
    args = 'no args for this command'
    help = 'Creates top and main banners'

    def handle(self, *args, **options):
        banner, _ = models.Banner.objects.get_or_create(name='main')
        if not banner.images.count():
            for index, image in enumerate(self._get_test_images()):
                banner.images.create(photo=image, description='image#{}'.format(index), link='http://google.com/')

    def _get_test_images(self):
        path = os.path.join(settings.BASE_DIR, 'gallery', 'management', 'commands', 'testimages')
        images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return [File(open(os.path.join(path, image))) for image in images]
