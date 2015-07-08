from . import models

FILTER_MODELS = (
    models.NumericAttributeFilter,
    models.ChoicesAttributeFilter,
    models.IntervalsAttributeFilter,
)


def update_filters_on_product_attribute_change(sender, instance, **kwargs):
    product_attribute = instance
    product = product_attribute.product_configuration.product
    characteristic = product_attribute.characteristic
    if characteristic is None:
        return

    for filter_model in FILTER_MODELS:
        for filt in filter_model.objects.for_product(product).filter(
                characteristic=characteristic, is_auto_update=True):
            filt.update()


def delete_filters_on_characteristic_disconnection_with_section(sender, instance, **kwargs):
    characteristic = instance.characteristic
    section = instance.section

    for filter_model in FILTER_MODELS:
        filter_model.objects.filter(characteristic=characteristic, section=section).delete()


def delete_filters_on_characteristic_disconnection_with_category(sender, instance, **kwargs):
    characteristic = instance.characteristic
    category = instance.category

    for filter_model in FILTER_MODELS:
        filter_model.objects.filter(characteristic=characteristic, category=category).delete()


def delete_filters_on_characteristic_disconnection_with_subcategory(sender, instance, **kwargs):
    characteristic = instance.characteristic
    subcategory = instance.subcategory

    for filter_model in FILTER_MODELS:
        filter_model.objects.filter(characteristic=characteristic, subcategory=subcategory).delete()
