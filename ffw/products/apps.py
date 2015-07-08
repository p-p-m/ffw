# coding: utf-8
from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _

from . import handlers, models


class ProductsConfig(AppConfig):
    name = 'products'
    verbose_name = _("Products and Categories")

    def ready(self):
        signals.post_migrate.connect(
            handlers.create_default_charachteristics,
            sender=self,
            dispatch_uid='products.handlers.create_default_charachteristics',
        )

        signals.post_save.connect(
            handlers.add_default_characteristics_to_new_section,
            sender=models.Section,
            dispatch_uid='products.handlers.add_default_characteristics_to_new_section'
        )

        signals.post_save.connect(
            handlers.add_new_default_characteristics_to_all_sections,
            sender=models.Characteristic,
            dispatch_uid='products.handlers.add_new_default_characteristics_to_all_categories',
        )
