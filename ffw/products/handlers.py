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
    instance.attributes.create(name='price_uah', value=instance.price_uah)
    instance.attributes.create(name='price_usd', value=instance.price_usd)
    instance.attributes.create(name='price_eur', value=instance.price_eur)
