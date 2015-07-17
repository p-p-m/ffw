# coding: utf-8
from __future__ import unicode_literals

from . import models

ATTRIBUTE_FILTER_MODELS = (
    models.NumericAttributeFilter,
    models.ChoicesAttributeFilter,
    models.IntervalsAttributeFilter,
)

FILTER_MODELS = ATTRIBUTE_FILTER_MODELS + (models.NumericPriceFilter, )


def update_filters_on_product_attribute_change(sender, instance, **kwargs):
    product_attribute = instance
    product = product_attribute.product_configuration.product
    characteristic = product_attribute.characteristic
    if characteristic is None:
        return

    for filter_model in ATTRIBUTE_FILTER_MODELS:
        for filt in filter_model.objects.for_product(product).filter(
                characteristic=characteristic, is_auto_update=True):
            filt.update()


def update_price_filter_on_price_change(sender, instance, **kwargs):
    product_configuration = instance
    for filt in models.NumericPriceFilter.objects.for_product(product_configuration.product).filter():
        filt.update()


def delete_filters_on_characteristic_disconnection_with_section(sender, instance, **kwargs):
    characteristic = instance.characteristic
    section = instance.section

    for filter_model in ATTRIBUTE_FILTER_MODELS:
        filter_model.objects.filter(characteristic=characteristic, section=section).delete()


def delete_filters_on_characteristic_disconnection_with_category(sender, instance, **kwargs):
    characteristic = instance.characteristic
    category = instance.category

    for filter_model in ATTRIBUTE_FILTER_MODELS:
        filter_model.objects.filter(characteristic=characteristic, category=category).delete()


def delete_filters_on_characteristic_disconnection_with_subcategory(sender, instance, **kwargs):
    characteristic = instance.characteristic
    subcategory = instance.subcategory

    for filter_model in ATTRIBUTE_FILTER_MODELS:
        filter_model.objects.filter(characteristic=characteristic, subcategory=subcategory).delete()


def autocreate_price_filter_for_section(sender, instance, created=False, **kwargs):
    if created:
        models.NumericPriceFilter.objects.create(name='Цена', section=instance, is_auto_update=True)
