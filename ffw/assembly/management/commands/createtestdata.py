# coding: utf-8
from __future__ import unicode_literals

import os
import random

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify

from products import models as products_models


class Command(BaseCommand):
    args = 'no args for this command'
    help = 'Creates '

    CHARACTERISTICS = [
        {
            'name': 'weight',
            'units': 'kg',
            'default_value': 0,
        },
        {
            'name': 'width',
            'units': 'm',
            'default_value': 0,
        },
        {
            'name': 'height',
            'units': 'm',
            'default_value': 0,
        },
        {
            'name': 'brand',
            'units': '',
            'default_value': '',
        }
    ]

    SECTIONS = [
        {
            'name': 'Filters for water',
            'categories': [
                {
                    'name': 'Big water filters',
                    'subcategories': [
                        {
                            'name': 'Big blue water filters'
                        },
                        {
                            'name': 'Big red water filters'
                        },
                        {
                            'name': 'Big green water filters'
                        }
                    ]
                },
                {
                    'name': 'Normal water filters',
                    'subcategories': [
                        {
                            'name': 'Normal yellow water filters'
                        },
                        {
                            'name': 'Normal magenta water filters'
                        },
                        {
                            'name': 'Normal purple water filters'
                        }
                    ]
                },
                {
                    'name': 'Small water filters',
                    'subcategories': [
                        {
                            'name': 'Small white water filters'
                        },
                        {
                            'name': 'Small black water filters'
                        },
                        {
                            'name': 'Small orange water filters'
                        }
                    ]
                },

            ]
        },
        {
            'name': 'Pools',
            'categories': [
                {
                    'name': 'Big pools',
                    'subcategories': [
                        {
                            'name': 'Big blue pools'
                        },
                        {
                            'name': 'Big red pools'
                        },
                        {
                            'name': 'Big green pools'
                        }
                    ]
                },
                {
                    'name': 'Normal pools',
                    'subcategories': [
                        {
                            'name': 'Normal yellow pools'
                        },
                        {
                            'name': 'Normal magenta pools'
                        },
                        {
                            'name': 'Normal purple pools'
                        }
                    ]
                },
                {
                    'name': 'Small pools',
                    'subcategories': [
                        {
                            'name': 'Small white pools'
                        },
                        {
                            'name': 'Small black pools'
                        },
                        {
                            'name': 'Small orange pools'
                        }
                    ]
                },

            ]
        },
    ]

    def _get_test_image(self):
        path = os.path.join(settings.BASE_DIR, 'assembly', 'management', 'commands', 'testimages')
        images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return File(open(os.path.join(path, random.choice(images))))

    def _create_characteristics(self):
        self.stdout.write('Creating characteristics...')
        for characteristic_data in self.CHARACTERISTICS:
            if not products_models.Characteristic.objects.filter(name=characteristic_data['name']).exists():
                characteristic = products_models.Characteristic.objects.create(**characteristic_data)
                self.stdout.write('Characteristic {} created'.format(characteristic))
        self.stdout.write('...Done')

    def _create_categories(self):
        self.stdout.write('Creating sections, categories and subcategories...')
        for section_data in self.SECTIONS:
            if not products_models.Section.objects.filter(name=section_data['name']).exists():
                categories = section_data.pop('categories')
                section = products_models.Section.objects.create(slug=slugify(section_data['name']), **section_data)
                self.stdout.write('Section {} created'.format(section))
                for category_data in categories:
                    subcategories = category_data.pop('subcategories')
                    category = products_models.Category.objects.create(
                        section=section,
                        slug=slugify(category_data['name']),
                        image=self._get_test_image(),
                        **category_data)
                    self.stdout.write('Category {} created'.format(category))
                    for subcategory_data in subcategories:
                        subcategory = products_models.Subcategory.objects.create(
                            category=category,
                            slug=slugify(subcategory_data['name']),
                            image=self._get_test_image(),
                            **subcategory_data)
                        self.stdout.write('Subcategory {} created'.format(subcategory))
        self.stdout.write('...Done')

    def _create_users(self):
        get_user_model().objects.all().delete()
        get_user_model().objects.create_superuser(username='admin', password='admin', email='admin@i.ua')
        self.stdout.write('Superuser admin/admin created')

    def _create_products(self):
        self.stdout.write('Creating products...')
        for index, subcategory in enumerate(products_models.Subcategory.objects.all()):
            self.stdout.write('Creating products for subcategory {}'.format(subcategory))
            for i in range(3):
                product = products_models.Product.objects.create(
                    name='product-{}-{}'.format(subcategory.id, i),
                    short_description='product-short-description-{}-{}'.format(subcategory.id, i),
                    description='product-description-{}-{}'.format(subcategory.id, i),
                    subcategory=subcategory,
                )
                for j in range(3 if not index else 1):
                    product_configuration = products_models.ProductConfiguration.objects.create(
                        product=product,
                        code='pc-{}-{}-{}'.format(index, i, j),
                    )
                    product_configuration.price_uah = 10 * (index + 1) * (i + 1) * (j + 1)
                    product_configuration.attrs.brand = random.choice(['B1', 'B2', 'B3', 'B4', 'B5'])
            self.stdout.write('Products created')
        self.stdout.write('...Done')

    def handle(self, *args, **options):
        self._create_characteristics()
        self._create_categories()
        self._create_users()
        self._create_products()
