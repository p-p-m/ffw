# coding: utf-8
from __future__ import unicode_literals

from django.apps import AppConfig
from django.db import signals
from django.utils.translation import ugettext_lazy as _


class ProductsConfig(AppConfig):
    name = 'products'
    verbose_name = _("Products and Categories")

    def ready(self):
        pass
