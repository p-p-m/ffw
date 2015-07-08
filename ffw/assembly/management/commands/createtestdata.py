# coding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify

from products import models as products_models
from products.tests import factories as products_factories


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

    def handle(self, *args, **options):
        self.stdout.write('Creating characteristics...')
        for characteristic_data in self.CHARACTERISTICS:
            if not products_models.Characteristic.objects.filter(name=characteristic_data['name']).exists():
                characteristic = products_models.Characteristic.objects.create(**characteristic_data)
                self.stdout.write('Characteristic {} created'.format(characteristic))
        self.stdout.write('...Done')

        self.stdout.write('Creating sections, categories and subcategories...')
        for section_data in self.SECTIONS:
            if not products_models.Section.objects.filter(name=section_data['name']).exists():
                categories = section_data.pop('categories')
                section = products_models.Section.objects.create(slug=slugify(section_data['name']), **section_data)
                self.stdout.write('Section {} created'.format(section))
                for category_data in categories:
                    subcategories = category_data.pop('subcategories')
                    category = products_models.Category.objects.create(
                        section=section, slug=slugify(category_data['name']), **category_data)
                    self.stdout.write('Category {} created'.format(category))
                    for subcategory_data in subcategories:
                        subcategory = products_models.Subcategory.objects.create(
                            category=category,  slug=slugify(subcategory_data['name']), **subcategory_data)
                        self.stdout.write('Subcategory {} created'.format(subcategory))
        self.stdout.write('...Done')

        # admin
        get_user_model().objects.all().delete()
        get_user_model().objects.create_superuser(username='admin', password='admin', email='admin@i.ua')
        self.stdout.write('Superuser admin/admin created')

        # TODO: add products
