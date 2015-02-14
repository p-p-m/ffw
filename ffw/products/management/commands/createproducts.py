# coding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from products import models
from products.tests import factories


class Command(BaseCommand):
    args = 'no args for this command'
    help = 'Creates '

    def handle(self, *args, **options):
        models.Product.objects.all().delete()
        models.Category.objects.all().delete()
        models.Subcategory.objects.all().delete()

        names = ['Фильтры для питьевой воды', 'Фильтры для басейнов', 'Фильтры для аквариумов']
        categories = [factories.CategoryFactory(name=name) for name in names]

        names = ['Грубые фильтры', 'Фильтры для усиленой очистки', 'Универсальные фильтры']
        subcategories = []
        for category in categories:
            subcategories += [factories.SubcategoryFactory(name=name, category=category) for name in names]

        for subcategory in subcategories:
            for _ in range(20):
                factories.ProductFactory(subcategory=subcategory)
