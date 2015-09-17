# coding: utf-8
from __future__ import unicode_literals

import os
import uuid

from django.db import models
from django.template.defaultfilters import slugify
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from unidecode import unidecode


class ImageFieldWaterMark(models.ImageField):

    def __init__(
            self, verbose_name=None, name=None, width_field=None, height_field=None,
            mark_text="p-p-m/ffw", font='DejaVuSerif-Bold.ttf', angle=23, opacity=0.25, **kwargs):
        self.angle = angle
        self.opacity = opacity
        self.mark_text = mark_text
        self.font = font
        kwargs['upload_to'] = safe_upload
        super(ImageFieldWaterMark, self).__init__(verbose_name, name, width_field=None, height_field=None, **kwargs)

    def pre_save(self, model_instance, add):
        file = super(ImageFieldWaterMark, self).pre_save(model_instance, add)
        if file:
            self.__add_watermark(file.path)
        return file

    def __add_watermark(self, file_path):
        img = Image.open(file_path).convert('RGB')
        watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
        size = 2
        n_font = ImageFont.truetype(self.font, size)
        n_width, n_height = n_font.getsize(self.mark_text)

        while n_width + n_height < watermark.size[0]:
            size += 2
            n_font = ImageFont.truetype(self.font, size)
            n_width, n_height = n_font.getsize(self.mark_text)

        draw = ImageDraw.Draw(watermark, 'RGBA')
        draw.text(
            ((watermark.size[0] - n_width) / 2, (watermark.size[1] - n_height) / 2),
            self.mark_text, font=n_font)
        watermark = watermark.rotate(self.angle, Image.BICUBIC)
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(self.opacity)
        watermark.putalpha(alpha)
        Image.composite(watermark, img, watermark).save(file_path, 'JPEG')


def safe_upload(instance, filename):
    name, ext = filename.split('.')
    name = slugify(unidecode(name))
    if not name:
        name = uuid.uuid4().hex
    filename = '{}.{}'.format(name, ext)
    return os.path.join('wm_images', filename)
