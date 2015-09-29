from . import models


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


def add_characteristic_to_category_subcategories(sender, instance, created=False, **kwargs):
    if created:
        for subcategory in instance.category.subcategories.all():
            models.SubcategoryCharacteristic.objects.get_or_create(
                characteristic=instance.characteristic,
                subcategory=subcategory
            )


def remove_characteristic_from_category_subcategories(sender, instance, **kwargs):
    (models.SubcategoryCharacteristic.objects
     .filter(characteristic=instance.characteristic, subcategory__in=instance.category.subcategories.all())
     .delete())


def add_characteristic_to_section_categories_and_subcategories(sender, instance, created=False, **kwargs):
    if created:
        for category in instance.section.categories.all():
            models.CategoryCharacteristic.objects.get_or_create(
                characteristic=instance.characteristic,
                category=category
            )

        for subcategory in models.Subcategory.objects.filter(category__in=instance.section.categories.all()):
            models.SubcategoryCharacteristic.objects.get_or_create(
                characteristic=instance.characteristic,
                subcategory=subcategory
            )


def remove_characteristic_from_section_categories_and_subcategories(sender, instance, **kwargs):
    (models.CategoryCharacteristic.objects
     .filter(characteristic=instance.characteristic, category__in=instance.section.categories.all())
     .delete())

    (models.SubcategoryCharacteristic.objects
     .filter(characteristic=instance.characteristic, subcategory__category__in=instance.section.categories.all())
     .delete())
