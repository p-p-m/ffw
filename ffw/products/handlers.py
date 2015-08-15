from . import models


def add_new_default_characteristics_to_all_sections(sender, instance=None, created=False, **kwargs):
    if created and instance.is_default:
        for section in models.Section.objects.all():
            section.characteristics.through.objects.create(characteristic=instance, section=section)


def add_default_characteristics_to_new_section(sender, instance=None, created=False, **kwargs):
    if created:
        for c in models.Characteristic.objects.filter(is_default=True):
            instance.characteristics.through.objects.create(characteristic=c, section=instance)


def calculate_price_attributes(sender, instance=None, **kwargs):
    product = instance.product
    product.recalculate_prices()
    product.save()


def connect_attribute_with_characteristic(sender, instance, **kwargs):
    attribute = instance
    if not attribute.characteristic:
        attribute.connect_with_characteristic()


def disconnect_attributes_from_characteristics_on_subcategory_change(sender, instance, **kwargs):
    product = instance
    # if subcategory changed
    if models.Product.objects.filter(id=product.id).exclude(subcategory=product.subcategory).exists():
        for attribute in models.ProductAttribute.objects.filter(product_configuration__product=product):
            attribute.connect_with_characteristic(subcategory=product.subcategory, save=True)
