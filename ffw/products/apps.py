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
            handlers.calculate_price_attributes,
            sender=models.ProductConfiguration,
            dispatch_uid='products.handlers.calculate_price_attributes',
        )

        signals.post_delete.connect(
            handlers.calculate_price_attributes,
            sender=models.ProductConfiguration,
            dispatch_uid='products.handlers.calculate_price_attributes',
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

        signals.post_save.connect(
            handlers.add_characteristic_to_category_subcategories,
            sender=models.CategoryCharacteristic,
            dispatch_uid='products.handlers.add_characteristic_to_category_subcategories'
        )

        signals.pre_delete.connect(
            handlers.remove_characteristic_from_category_subcategories,
            sender=models.CategoryCharacteristic,
            dispatch_uid='products.handlers.remove_characteristic_from_category_subcategories'
        )

        signals.post_save.connect(
            handlers.add_characteristic_to_section_categories_and_subcategories,
            sender=models.SectionCharacteristic,
            dispatch_uid='products.handlers.add_characteristic_to_section_categories_and_subcategories'
        )

        signals.pre_delete.connect(
            handlers.remove_characteristic_from_section_categories_and_subcategories,
            sender=models.SectionCharacteristic,
            dispatch_uid='products.handlers.remove_characteristic_from_section_categories_and_subcategories'
        )
