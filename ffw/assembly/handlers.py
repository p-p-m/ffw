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
        models.NumericPriceFilter.objects.create(name='Цена', section=instance, is_auto_update=True, priority=100)


def autocreate_price_filter_for_category(sender, instance, created=False, **kwargs):
    if created:
        models.NumericPriceFilter.objects.create(name='Цена', category=instance, is_auto_update=True, priority=100)


def autocreate_price_filter_for_subcategory(sender, instance, created=False, **kwargs):
    if created:
        models.NumericPriceFilter.objects.create(name='Цена', subcategory=instance, is_auto_update=True, priority=100)


def propagate_filter_to_subcategories_and_categories(sender, instance, created=False, **kwargs):
    if created:
        if instance.section is not None:
            for category in instance.section.categories.all():
                sender.objects.get_or_create(
                    name=instance.name,
                    characteristic=instance.characteristic,
                    category=category,
                    is_auto_update=instance.is_auto_update,
                )

        if instance.category is not None:
            for subcategory in instance.category.subcategories.all():
                sender.objects.get_or_create(
                    name=instance.name,
                    characteristic=instance.characteristic,
                    subcategory=subcategory,
                    is_auto_update=instance.is_auto_update,
                )


def delete_filters_from_related_subcategories_and_categories(sender, instance, created=False, **kwargs):
    if instance.section is not None:
        (sender.objects
         .filter(name=instance.name,
                 characteristic=instance.characteristic,
                 category__in=instance.section.categories.all())
         .delete())

    if instance.category is not None:
        (sender.objects
         .filter(name=instance.name,
                 characteristic=instance.characteristic,
                 subcategory__in=instance.category.subcategories.all())
         .delete())
