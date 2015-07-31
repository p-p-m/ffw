from . import models


def add_new_default_characteristics_to_all_sections(sender, instance=None, created=False, **kwargs):
    if created and instance.is_default:
        for section in models.Section.objects.all():
            section.characteristics.through.objects.create(characteristic=instance, section=section)


def add_default_characteristics_to_new_section(sender, instance=None, created=False, **kwargs):
    if created:
        for c in models.Characteristic.objects.filter(is_default=True):
            instance.characteristics.through.objects.create(characteristic=c, section=instance)


def create_price_attributes(sender, instance=None, **kwargs):
    product = instance.product
    if product.price_min > instance.price_uah or product.price_min is None:
        product.price_min = instance.price_uah
        product.save()

    if product.price_max < instance.price_uah or product.price_max is None:
        product.price_max = instance.price_uah
        product.save()


def connect_attribute_with_characteristic(sender, instance, **kwargs):
    attribute = instance
    if not attribute.characteristic:
        try:
            c = models.Characteristic.objects.get(name=attribute.name)
            attribute.characteristic = c
            attribute.units = c.units
        except models.Characteristic.DoesNotExist:
            pass
