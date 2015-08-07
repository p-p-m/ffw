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
        signals.post_save.connect(
            handlers.create_price_attributes,
            sender=models.ProductConfiguration,
            dispatch_uid='products.handlers.create_price_attributes',
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

        signals.pre_save.connect(
            handlers.connect_attribute_with_characteristic,
            sender=models.ProductAttribute,
            dispatch_uid='products.handlers.connect_attribute_with_characteristic',
        )

        signals.pre_save.connect(
            handlers.disconnect_attributes_from_characteristics_on_subcategory_change,
            sender=models.Product,
            dispatch_uid='products.handlers.disconnect_attributes_from_characteristics_on_subcategory_change'
        )
