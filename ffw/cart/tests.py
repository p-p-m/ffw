# coding: utf-8
import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from products.models import Subcategory, Category, Section, Product, ProductConfiguration


class CartViewTest(TestCase):

    def setUp(self):
        section = Section.objects.create(name="Home", slug='Home')
        category = Category.objects.create(name="Electro", slug="electro", section=section)
        subcategory =Subcategory.objects.create(name="Iron", slug="iron", category=category)
        product = Product.objects.create(name="product-1", short_description = 'hdhfrj', subcategory=subcategory)
        ProductConfiguration.objects.create(product=product, code="code-1", price_uah=20, pk=1)
        ProductConfiguration.objects.create(product=product, code="code-2", price_uah=70, pk=2)
        ProductConfiguration.objects.create(product=product, code="code-3", price_uah=110, pk=3)
        ProductConfiguration.objects.create(product=product, code="code-4", price_uah=200, pk=4)

    def test_cart(self):
        self._testing_cart_get()
        # test CartSetView
        self.msg = "CartSetView is invalid"
        self.url_name = 'cart_set'
        self.product_dict = {1: 2, 2: 3} #add to cart of session
        self.product_cart = {1: 2, 2: 3}  #add to cart of test
        self.data_cart = {'total': 250, 'count': 5} #add to cart of test
        self._get_cart()
        # test CartAddView
        self.msg = "CartAddView is invalid"
        self.url_name = 'cart_add'
        self.product_dict = {1: 4, 2: 2, 3: 3, 4: 1} #add to cart of session
        self.product_cart = {1: 6, 2: 5, 3: 3, 4: 1}  #add to cart of test
        self.data_cart = {'total': 1000, 'count':15} #add to cart of test
        self._get_cart()
        # test CartRemoveView
        self.msg = "CartRemoveView is invalid"
        self.url_name = 'cart_remove'
        self.product_dict ={1: 0, 2:0} #add to cart of session
        self.product_cart = {3: 3, 4: 1} #add to cart of test
        self.data_cart = {'total': 530, 'count': 4} #add to cart of test
        self._get_cart()
        # test CartView.post() -clear cart
        self.msg = "CartView.post()  is invalid"
        self.url_name = 'cart'
        self.product_dict ={} #add to cart of session
        self.product_cart = {} #add to cart of test
        self.data_cart = {'total': 0, 'count': 0} #add to cart of test
        self._get_cart()

    def _testing_cart_get(self):
        self.msg = "CartView.get()  is invalid"
        self.url_name = 'cart'
        self.cart={'products': {}, 'count': 0, 'total': 0}
        self._compare_cart()

    def _get_cart(self):
        self.cart={'products': {}, 'count': 0, 'total': 0}

        for product_pk in self.product_cart:
            product = ProductConfiguration.objects.get(pk=product_pk)
            quant =  self.product_cart[product.pk]
            price =  float(product.price_uah)
            self.cart['products'][str(product.pk)] = {
                'quant': quant,
                'name': product.product.name,
                'product_code': product.code,
                'price': price,
                'sum_': float(price * quant)}

        self.cart['count'] = self.data_cart['count']
        self.cart['total'] = self.data_cart['total']

        if self.url_name == 'cart_remove':
            product_pk_list = [product_pk for product_pk in self.product_dict]
            self.client.post(reverse(self.url_name), {'product_pk_list': json.dumps(product_pk_list)})
        else:
            self.client.post(reverse(self.url_name), {'product_dict': json.dumps(self.product_dict)})

        self._compare_cart()

    def _compare_cart(self):
        response = self.client.get(reverse("cart"))
        self.cart_session = json.loads(response.content)['cart']
        self.assertDictEqual(self.cart, self.cart_session, msg=self.msg)
