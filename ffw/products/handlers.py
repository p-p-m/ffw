from . import models


def add_new_default_characteristics_to_all_categories(sender, instance=None, created=False, **kwargs):
    if created and instance.is_default:
        for model in models.PRODUCT_CATEGORIES_MODELS:
            for category in model.objects.all():
                category.characteristics.add(instance)


def add_default_characteristics_to_new_categories(sender, instance=None, created=False, **kwargs):
    if created:
        instance.characteristics.add(*list(models.Characteristic.objects.filter(is_default=True)))
