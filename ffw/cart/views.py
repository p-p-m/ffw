#  -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

import models
from products.models import Product
from django.utils.translation import ugettext_lazy as _

from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from products.models import Product
from models import TestProduct
from django.conf import settings

class CSRFProtectMixin():
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
         return super(CartSet, self).dispatch(*args, **kwargs)


class CartClearMixin():

    def cart_clear(self, session):
        if 'products_cart' in session :
            del session['products_cart']
        if 'sum_cart' in session :
            del session['sum_cart']
        if 'count_cart' in session :
            del session['count_cart']


class CartResultMixin(View, CSRFProtectMixin, CartClearMixin):

    def format_response(self, session):
        if 'products_cart' in session:
            if session["products_cart"] == {}:
                self.cart_clear(session)
                sum_cart = 0
                count_cart = 0
                products_cart = {}
            else:
                session['sum_cart'] = round(sum(
                    [v['sum_'] for v in session['products_cart'].values()]), 2)
                session['count_cart'] = sum(
                    [v['quant'] for v in session['products_cart'].values()])

                count_cart = session['count_cart']
                sum_cart = session['sum_cart']
                products_cart = session['products_cart']
        else:
            self.cart_clear(session)
            sum_cart = 0
            count_cart = 0
            products_cart = {}


        return HttpResponse(json.dumps({'sum_cart': sum_cart, 'count_cart':
                count_cart, 'products_cart': products_cart}))


class CartRemoveView(CartResultMixin):

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            product_pk = request.POST.get('product_pk', '')

            if product_pk in request.session["products_cart"]:
                del request.session["products_cart"][product_pk]

            return self.format_response(request.session)


class CartView(CartResultMixin, CartClearMixin):

    def get(self, request, *args, **kwargs):
        if request.is_ajax:
            print(getattr(settings, 'CART_SETTINGS'),222)
            return self.format_response(request.session)


    def post(self, request, *args, **kwargs):
        '''
        Clear cart
        '''
        if request.is_ajax:
            self.cart_clear(request.session)

            return self.format_response(request.session)


class CartTestView(TemplateView):
    '''
    For test
    '''

    template_name = 'cart_test.html'

    def get_context_data(self, **kwargs):
        context = super(CartTestView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class CartSetView(CartResultMixin):
    '''
    Super for CartAddView
    '''
    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            session = request.session
            session['products_cart'] = session.get('products_cart', {})

            product_pk = request.POST.get('product_pk', '')
            test = request.POST.get("test", False)
            try:
                quant = int(request.POST.get('quant', '0'))
            except ValueError:
                quant = 0
            if test == False:
                product = get_object_or_404(Product.objects, pk=product_pk)
            else:
                 product = get_object_or_404(TestProduct.objects, pk=product_pk)
            if quant <= 0:
                if product_pk in session["products_cart"]:
                    self.change_session(session["products_cart"], product_pk)
            else:
                price = float(product.price_uah)
                name = product.name
                product_code = product.code
                quant = self.calc_quant(session, product_pk, quant)
                sum_ = round( quant * price, 2)

                session['products_cart'][product_pk] = {
                    'product_code': product_code,
                    'name': name,
                    'price': price,
                    'quant': quant,
                    'sum_': sum_}

        return self.format_response(session)

    def change_session(self, products_cart, product_pk):
        products_cart.pop(product_pk)

    def calc_quant(self, session, product_pk, quant):
        return quant


class CartAddView(CartSetView):

    def change_session(self, products_cart, product_pk):
        pass

    def calc_quant(self, session, product_pk, quant):
        if product_pk in session["products_cart"]:
            quant += session["products_cart"][product_pk]['quant']
        return quant
