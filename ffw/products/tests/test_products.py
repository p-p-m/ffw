from django.test import TestCase

from ..models import Category, Subcategory


class SomeTest(TestCase):

    def test_one_equals_one(self):
        self.assertEqual(1, 1)
