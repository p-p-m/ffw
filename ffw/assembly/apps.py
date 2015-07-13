# coding: utf-8
from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _

from products import models as products_models
from . import handlers


class AssemblyConfig(AppConfig):
    name = 'assembly'
    verbose_name = _('Assembly')

    def ready(self):
        signals.post_save.connect(
            handlers.update_filters_on_product_attribute_change,
            sender=products_models.ProductAttribute,
            dispatch_uid='assembly.handlers.update_filters_on_product_attribute_change',
        )

        signals.post_delete.connect(
            handlers.delete_filters_on_characteristic_disconnection_with_section,
            sender=products_models.SectionCharacteristic,
            dispatch_uid='assembly.handlers.delete_filters_on_characteristic_disconnection_with_section',
        )

        signals.post_delete.connect(
            handlers.delete_filters_on_characteristic_disconnection_with_category,
            sender=products_models.CategoryCharacteristic,
            dispatch_uid='assembly.handlers.delete_filters_on_characteristic_disconnection_with_category',
        )

        signals.post_delete.connect(
            handlers.delete_filters_on_characteristic_disconnection_with_subcategory,
            sender=products_models.SubcategoryCharacteristic,
            dispatch_uid='assembly.handlers.delete_filters_on_characteristic_disconnection_with_subcategory',
        )

        signals.post_save.connect(
            handlers.autocreate_price_filter_for_section,
            sender=products_models.Section,
            dispatch_uid='assembly.handlers.autocreate_price_filter_for_section'
        )
