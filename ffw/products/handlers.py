from . import models


def add_new_default_characteristics_to_all_sections(sender, instance=None, created=False, **kwargs):
    if created and instance.is_default:
        for section in models.Section.objects.all():
            section.characteristics.through.objects.create(characteristic=instance, section=section)


def add_default_characteristics_to_new_section(sender, instance=None, created=False, **kwargs):
    if created:
        for c in models.Characteristic.objects.filter(is_default=True):
            instance.characteristics.through.objects.create(characteristic=c, section=instance)


def create_default_charachteristics(sender, **kwargs):
    models.Characteristic.objects.get_or_create(name='price_uah', default_value=0, units='UAH', is_default=True)
    models.Characteristic.objects.get_or_create(name='price_usd', default_value=0, units='USD', is_default=True)
    models.Characteristic.objects.get_or_create(name='price_eur', default_value=0, units='EUR', is_default=True)
