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
        #Test CartView.get(), CartSetView, CartAddView, CartRemoveView and CartView.post()
        #self.cart - cart for control by comparing with session['cart']
        #self.product_dict and  self.product_cart - dictionary with key=product.pk and value=quant
        #self.data_cart - dictionary with total data for self.cart
        #self.product_dict - use for create  session['cart']
        #self.product_cart and self.data_cart -  use for create  self.cart

        #test CartView.get() - get session['cart']
        self.msg = "CartView.get()  is invalid"
        self.url_name = 'cart'
        self.cart={'products': {}, 'count': 0, 'total': 0}
        self._compare_cart()

        # test CartSetView
        self.msg = "CartSetView is invalid"
        self.url_name = 'cart_set'
        self.product_dict = {1: 2, 2: 3}
        self.product_cart = {1: 2, 2: 3}
        self.data_cart = {'total': 250, 'count': 5}

        self._calc('product_dict', self.product_dict)

        # test CartAddView
        self.msg = "CartAddView is invalid"
        self.url_name = 'cart_add'
        self.product_dict = {1: 4, 2: 2, 3: 3, 4: 1}
        self.product_cart = {1: 6, 2: 5, 3: 3, 4: 1}
        self.data_cart = {'total': 1000, 'count':15}

        self._calc('product_dict', self.product_dict)

        # test CartRemoveView
        self.msg = "CartRemoveView is invalid"
        self.url_name = 'cart_remove'
        self.product_dict ={1: 0, 2:0}
        self.product_cart = {3: 3, 4: 1}
        self.data_cart = {'total': 530, 'count': 4}
        product_pk_list = [product_pk for product_pk in self.product_dict]

        self._calc('product_pk_list', product_pk_list)

        # test CartView.post() -clear cart
        self.msg = "CartView.post()  is invalid"
        self.url_name = 'cart'
        self.product_dict ={}
        self.product_cart = {}
        self.data_cart = {'total': 0, 'count': 0}

        self._calc('product_dict', self.product_dict)

    def _calc(self, key, value):
        self.client.post(reverse(self.url_name), {key: json.dumps(value)}) #send request.post
        self._get_cart() #get self.cart
        self._compare_cart() #control by comparing session['cart'] with self.cart

    def _get_cart(self):
        #create cart for control by comparing with session['cart']
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

    def _compare_cart(self):
        #control by comparing session['cart'] with self.cart
        response = self.client.get(reverse("cart")) #send request to get session['cart']
        session_cart = json.loads(response.content)['cart']
        self.assertDictEqual(self.cart, session_cart, msg=self.msg)
