# coding: utf-8
import difflib  # for assertDictEqual in CartViewTest
import json
import pprint  # for assertDictEqual in CartViewTest

# for assertDictEqual in CartViewTest
from unittest.util import (
    strclass, safe_repr, unorderable_list_difference,
    _count_diff_all_purpose, _count_diff_hashable
)

from django.test import TestCase
from django.core.urlresolvers import reverse

from products.models import Subcategory, Category, Section, Product, ProductConfiguration


def factory(aClass, **kwargs):
    return aClass.objects.create(**kwargs)


class CartViewTest(TestCase):

    # mode_not_equal=False, products_changed=None
    def assertDictEqual(self, session_cart):
        self.assertIsInstance(
            self.expected_cart,
            dict,
            'First argument is not a dictionary')
        self.assertIsInstance(
            session_cart,
            dict,
            'Second argument is not a dictionary')

        if self.expected_cart != session_cart:
            standardMsg = '%s != %s' % (
                safe_repr(self.expected_cart, True), safe_repr(session_cart, True))
            diff = ('\n' + '\n'.join(difflib.ndiff(
                           pprint.pformat(self.expected_cart,).splitlines(),
                           pprint.pformat(session_cart).splitlines())))
            standardMsg = self._truncateMessage(standardMsg, diff)
            msg = '\n' * 2 + 'FAIL test_user_can_' + self.msg + '\n' * 2

            if self.session_cart_to_begin:
                msg += "The cart to begin:" + '\n' + \
                    json.dumps(self.session_cart_to_begin) + '\n' * 2

            if self.products_changed:
                msg += self.msg_1 + '\n' + \
                    json.dumps(self.products_changed) + '\n' * 2

            msg += "Expected cart:" + '\n' + \
                json.dumps(self.expected_cart) + '\n' * 2
            msg += 'Reseived cart:' + '\n' + json.dumps(session_cart)
            self.fail(self._formatMessage(msg, standardMsg))
        else:
            print "OK " + self.msg

    def setUp(self):
        # create section, category, subcategory, product, configuration
        section = factory(Section, name="Home", slug='Home')
        category = factory(Category, name="Electro", slug="electro",
                           section=section)
        subcategory = factory(Subcategory, name="Iron", slug="iron",
                              category=category)
        product = factory(Product, name="product-1", short_description='hdhfrj',
                          subcategory=subcategory)

        self.price_1 = 20
        self.price_2 = 70
        self.price_3 = 110
        self.price_4 = 200

        product_pk_tupple = ()

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

        self.session_cart_to_begin = {}
        self.products_changed = {}

    def test_cart(self):
        # Test url name "cart", "cart_set", "cart_add", "cart_remove", "cart_clear"
        # self.expected_cart - cart for control by comparing with session['cart']
        # self.product_dict - use for create  session['cart']
        # self.expected_products  -  use for create  self.expected_cart
        self.expected_quant_1 = 0
        self.expected_quant_2 = 0
        self.expected_quant_3 = 0
        self.expected_quant_4 = 0

        # The additional functions to comparing the expected cart with session[
        # create expected cart for control by comparing with session['cart']
        def create_expected_cart():
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

        # get session["cart"], control by comparing with self.expected_cart
        def compare_carts():
            response = self.client.get(reverse("cart"))
            session_cart = json.loads(response.content)['cart']
            self.assertDictEqual(session_cart)
            self.session_cart_to_begin = session_cart

        # send request.post, get self.expected_cart, call function to control
        # by comparing session['cart'] with self.expected_cart
        def calc(key, value):
            self.client.post(reverse(self.url_name),
                             {key: json.dumps(value)})
            create_expected_cart()
            compare_carts()

        # calculating total data of the expected cart
        def _total_data(quant_1=0, quant_2=0, quant_3=0, quant_4=0):
            self.expected_quant_1 += quant_1
            self.expected_quant_2 += quant_2
            self.expected_quant_3 += quant_3
            self.expected_quant_4 += quant_4
            self.expected_count = self.expected_quant_1 + self.expected_quant_2 + \
                self.expected_quant_3 + self.expected_quant_4
            self.expected_total = self.expected_quant_1 * self.price_1 + self.expected_quant_2 * self.price_2 + \
                self.expected_quant_3 * self.price_3 + self.expected_quant_4 * self.price_4
        # ______________________________ The additional functions to comparing
        # the expected cart with session['cart']

        # The test functions __________________________________________________
        # control getting the cart from session
        def cart_get_test():
            #self.session_cart_to_begin = {'products': {}, 'count': 0, 'total': 0}
            #self.products_changed = {}
            self.msg = '{0:24}, {1:2}'.format(
                "get_cart", "url name = 'cart' method GET")
            self.url_name = 'cart'
            self.expected_cart = {'products': {}, 'count': 0, 'total': 0}
            compare_carts()

        # control setting data to the session cart
        def cart_set_test():
            self.msg = '{0:24}, {1:25}'.format(
                "set_product_to_cart", "url name = 'cart_set'")
            self.msg_1 = "The setted products:"
            self.url_name = 'cart_set'
            quant_1 = 2
            quant_2 = 3

            self.product_dict = {
                self.product_pk_1: quant_1,
                self.product_pk_2: quant_2}

            _total_data(quant_1, quant_2)

            self.expected_products = {self.product_pk_1: self.expected_quant_1,
                                      self.product_pk_2: self.expected_quant_2}
            self.products_changed = {self.product_pk_1: {'quant': quant_1, 'price': self.price_1, 'sum': float(self.price_1 * quant_1)},
                                     self.product_pk_2: {'quant': quant_2, 'price': self.price_2, 'sum': float(self.price_2 * quant_2)}}
            calc('product_dict', self.product_dict)

        # control adding data to the session cart
        def cart_add_test():
            self.msg = '{0:24}, {1:25}'.format(
                "add_product_to_cart", "url name = 'cart_add")
            self.msg_1 = "The added products:"
            self.url_name = 'cart_add'
            quant_1 = 4
            quant_2 = 2
            quant_3 = 3
            quant_4 = 1
            self.product_dict = {self.product_pk_1: quant_1, self.product_pk_2: quant_2,
                                 self.product_pk_3: quant_3, self.product_pk_4: quant_4}

            _total_data(quant_1, quant_2, quant_3, quant_4)

            self.expected_products = {self.product_pk_1: self.expected_quant_1, self.product_pk_2: self.expected_quant_2,
                                      self.product_pk_3: self.expected_quant_3, self.product_pk_4: self.expected_quant_4}

            calc('product_dict', self.product_dict)

        # control removing products from the session cart
        def cart_remove_test():
            self.msg = '{0:24}, {1:25}'.format(
                "remove_product_from_cart", "url name = 'cart_remove'")
            self.msg_1 = "The removed products:"
            self.url_name = 'cart_remove'
            _total_data(- self.expected_quant_1, - self.expected_quant_2)
            self.expected_products = {
                self.product_pk_3: self.expected_quant_3,
                self.product_pk_4: self.expected_quant_4}

            calc('product_pk_list', [self.product_pk_1, self.product_pk_2])

        # control clearing the session cart
        def cart_clear_test():
            self.msg = '{0:24}, {1:25}'.format(
                "clear_cart", "url name = 'cart' method POST")
            self.url_name = 'cart'

            self.product_dict = {}
            self.products_changed = {}

            self.expected_products = {}
            self.expected_total = 0
            self.expected_count = 0

            calc('product_dict', self.product_dict)
       # _________________________________________________________________________________________
       # The test functions

        cart_get_test()
        cart_set_test()
        cart_add_test()
        cart_remove_test()
        cart_clear_test()
