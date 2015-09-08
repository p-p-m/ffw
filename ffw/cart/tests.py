# coding: utf-8
import difflib  # for assertDictEqual in TestCaseOwn
import json
import pprint  # for assertDictEqual in TestCaseOwn

# for assertDictEqual in TestCaseOwn
from unittest.util import (
    strclass, safe_repr, unorderable_list_difference,
    _count_diff_all_purpose, _count_diff_hashable
)

from django.test import TestCase
from django.core.urlresolvers import reverse

from products.models import Subcategory, Category, Section, Product, ProductConfiguration


def factory(aClass, **kwargs):
    return aClass.objects.create(**kwargs)


class TestCaseOwn(TestCase):

    def assertDictEqual(self, d1, d2, msg=None, mode_not_equal=False):
        self.assertIsInstance(d1, dict, 'First argument is not a dictionary')
        self.assertIsInstance(d2, dict, 'Second argument is not a dictionary')

        if d1 != d2:
            standardMsg = '%s != %s' % (
                safe_repr(d1, True), safe_repr(d2, True))
            diff = ('\n' + '\n'.join(difflib.ndiff(
                           pprint.pformat(d1).splitlines(),
                           pprint.pformat(d2).splitlines())))
            standardMsg = self._truncateMessage(standardMsg, diff)
            msg = ('\n' * 2 + 'FAIL test_user_can_' + msg + '\n' * 2 + ("Expected cart:" + '\n' + json.dumps(d1) + '\n' * 2 + 'Reseived cart:' +
                                                                        '\n' + json.dumps(d2)))
            self.fail(self._formatMessage(msg, standardMsg))
        else:
            print "OK " + msg


class CartViewTest(TestCaseOwn):

    def setUp(self):
        section = factory(Section, name="Home", slug='Home')
        category = factory(
            Category,
            name="Electro",
            slug="electro",
            section=section)
        subcategory = factory(
            Subcategory,
            name="Iron",
            slug="iron",
            category=category)
        product = factory(
            Product,
            name="product-1",
            short_description='hdhfrj',
            subcategory=subcategory)

        product_pk_tupple = ()
        self.price_1 = 20
        self.price_2 = 70
        self.price_3 = 110
        self.price_4 = 200

        for code, price in ['code-1', self.price_1], ['code-2',
                                                      self.price_2], ['code-3', self.price_3], ['code-4', self.price_4]:
            product_conf = factory(
                ProductConfiguration,
                product=product,
                code=code,
                price_uah=price)
            product_pk_tupple += (product_conf.pk,)

        self.product_pk_1 = product_pk_tupple[0]
        self.product_pk_2 = product_pk_tupple[1]
        self.product_pk_3 = product_pk_tupple[2]
        self.product_pk_4 = product_pk_tupple[3]

    def test_cart(self):
        # Test url name "cart", "cart_set", "cart_add", "cart_remove", "cart_clear"
        # self.expected_cart - cart for control by comparing with session['cart']
        # self.product_dict - use for create  session['cart']
        # self.expected_products  -  use for create  self.expected_cart
        self.expected_quant_1 = 0
        self.expected_quant_2 = 0
        self.expected_quant_3 = 0
        self.expected_quant_4 = 0

        def get_cart():
            # create cart for control by comparing with session['cart']
            self.expected_cart = {'products': {}, 'count': 0, 'total': 0}

            for product_pk in self.expected_products:
                product = ProductConfiguration.objects.get(pk=product_pk)
                quant = self.expected_products[product.pk]
                price = float(product.price_uah)
                self.expected_cart['products'][str(product.pk)] = {
                    'quant': quant,
                    'name': product.product.name,
                    'product_code': product.code,
                    'price': price,
                    'sum_': float(price * quant)}

            self.expected_cart['count'] = self.expected_count
            self.expected_cart['total'] = self.expected_total

        def compare_cart():
            # control by comparing session['cart'] with self.expected_cart
            # send request to get session['cart']
            response = self.client.get(reverse("cart"))
            session_cart = json.loads(response.content)['cart']
            self.assertDictEqual(self.expected_cart, session_cart, self.msg)

        def calc(key, value):
            self.client.post(reverse(self.url_name),
                             {key: json.dumps(value)})  # send request.post
            get_cart()  # get self.expected_cart
            # control by comparing session['cart'] with self.expected_cart
            compare_cart()

        def _total_data(quant_1=0, quant_2=0, quant_3=0, quant_4=0):
            self.expected_quant_1 += quant_1
            self.expected_quant_2 += quant_2
            self.expected_quant_3 += quant_3
            self.expected_quant_4 += quant_4
            self.expected_count = self.expected_quant_1 + self.expected_quant_2 + \
                self.expected_quant_3 + self.expected_quant_4
            self.expected_total = (self.expected_quant_1 * self.price_1 + self.expected_quant_2 * self.price_2 +
                                   self.expected_quant_3 * self.price_3 + self.expected_quant_4 * self.price_4)

        def cart_get_test():
            # method get
            self.msg = "get_cart"
            self.url_name = 'cart'
            self.expected_cart = {'products': {}, 'count': 0, 'total': 0}
            compare_cart()

        def cart_set_test():
            self.msg = "set_product_to_cart"
            self.url_name = 'cart_set'
            quant_1 = 2
            quant_2 = 3
            self.product_dict = {
                self.product_pk_1: quant_1,
                self.product_pk_2: quant_2}
            _total_data(quant_1, quant_2)
            self.expected_products = {
                self.product_pk_1: self.expected_quant_1,
                self.product_pk_2: self.expected_quant_2}

            calc('product_dict', self.product_dict)

        def cart_add_test():
            self.msg = "add_product_to_cart"
            self.url_name = 'cart_add'
            quant_1 = 4
            quant_2 = 2
            quant_3 = 3
            quant_4 = 1
            self.product_dict = {
                self.product_pk_1: quant_1,
                self.product_pk_2: quant_2,
                self.product_pk_3: quant_3,
                self.product_pk_4: quant_4}
            _total_data(quant_1, quant_2, quant_3, quant_4)
            self.expected_products = {self.product_pk_1: self.expected_quant_1, self.product_pk_2: self.expected_quant_2,
                                      self.product_pk_3: self.expected_quant_3, self.product_pk_4: self.expected_quant_4}

            calc('product_dict', self.product_dict)

        def cart_remove_test():
            self.msg = "remove_product_from_cart"
            self.url_name = 'cart_remove'
            _total_data(- self.expected_quant_1, - self.expected_quant_2)
            self.expected_products = {
                self.product_pk_3: self.expected_quant_3,
                self.product_pk_4: self.expected_quant_4}

            calc('product_pk_list', [self.product_pk_1, self.product_pk_2])

        def cart_clear_test():
            self.msg = "clear_cart"
            self.url_name = 'cart'
            self.product_dict = {}
            self.expected_products = {}
            self.expected_total = 0
            self.expected_count = 0

            calc('product_dict', self.product_dict)

        cart_get_test()
        cart_set_test()
        cart_add_test()
        cart_remove_test()
        cart_clear_test()
