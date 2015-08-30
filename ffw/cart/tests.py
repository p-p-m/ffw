# coding: utf-8
import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from products.models import Subcategory, Category, Section, Product, ProductConfiguration


def create_products():

    section = Section.objects.create(name="Home", slug='Home')
    category = Category.objects.create(name="Electro", slug="electro", section=section)
    subcategory =Subcategory.objects.create(name="Iron", slug="iron", category=category)
    product = Product.objects.create(name="product-1", short_description = 'hdhfrj', subcategory=subcategory)
    ProductConfiguration.objects.create(product=product, code="code-1", price_uah=100)
    ProductConfiguration.objects.create(product=product, code="code-2", price_uah=171)
    ProductConfiguration.objects.create(product=product, code="code-3", price_uah=106)

class CartViewTest(TestCase):
    def test_cart_view(self):
        create_products()
        product_dict = {}
        for product in ProductConfiguration.objects.all():
            product_dict[product.pk] = 1 + int(product.pk)

        print 'lllll - ',product_dict, json.dumps((product_dict))
        self.client.post(reverse("cart_set", kwargs={'product_dict': product_dict}))
        response = self.client.get(reverse("cart"))
        print 'response - ', response.context
        #self.assertQuerysetEqual(response.context.)

