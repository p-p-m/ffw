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
        models.Category.objects.all().delete()
        models.Subcategory.objects.all().delete()
        # admin
        get_user_model().objects.create_superuser(username='admin', password='admin', email='admin@i.ua')
        # categories
        categories = [factories.CategoryFactory() for _ in range(3)]
        # subcategories
        subcategories = []
        for category in categories:
            subcategories += [factories.SubcategoryFactory(category=category) for _ in range(3)]
        # products
        for subcategory in subcategories:
            for _ in range(20):
                factories.ProductFactory(subcategory=subcategory)
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
