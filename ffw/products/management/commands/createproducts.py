# coding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from products import models
from products.tests import factories


class Command(BaseCommand):
    args = 'no args for this command'
    help = 'Creates '

    def handle(self, *args, **options):
        models.Product.objects.all().delete()
        models.Section.objects.all().delete()
        models.Category.objects.all().delete()
        models.Subcategory.objects.all().delete()
        models.Characteristic.objects.all().delete()
        get_user_model().objects.all().delete()
        # admin
        get_user_model().objects.create_superuser(username='admin', password='admin', email='admin@i.ua')
        self.stdout.write('Superuser admin/admin was created successfully')
        # sections:
        sections = [factories.SectionFactory() for _ in range(3)]
        # categories
        categories = []
        for section in sections:
            categories += [factories.CategoryFactory(section=section) for _ in range(3)]
        # subcategories
        subcategories = []
        for category in categories:
            subcategories += [factories.SubcategoryFactory(category=category) for _ in range(3)]
        self.stdout.write('Sections, categories and subcategories were created successfully')
        characteristics = [factories.CharacteristicFactory.build() for _ in range(50)]
        models.Characteristic.objects.bulk_create(characteristics)
        self.stdout.write('Characteristics were created successfully')
        # products
        for subcategory in subcategories:
            models.Product.objects.bulk_create(
                [factories.ProductFactory.build(subcategory=subcategory) for _ in range(10)])
            self.stdout.write('Products for subcategory {} were created successfully'.format(subcategory))
        self.stdout.write('Products were created successfully')
        # filters:
        for category in categories:
            f = models.ProductFilter.objects.create(
                attribute_name='Height', filter_type='NUMERIC', category=category, name='Height filter')
            f.clean()
            f.save()
            f = models.ProductFilter.objects.create(
                attribute_name='Width', filter_type='NUMERIC_RANGES', category=category, name='Width filter')
            f.clean()
            f.save()
        self.stdout.write('Products filters were created successfully')
