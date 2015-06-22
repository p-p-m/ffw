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


class CSRFProtectMixin():
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
         return super(CartSet, self).dispatch(*args, **kwargs)


class CartResultMixin(View, CSRFProtectMixin):

    def format_response(self, session):
        if 'products_cart' in session:
            session['sum_cart'] = round(sum(
                [v['sum_'] for v in session['products_cart'].values()]), 2)
            sum_cart = session['sum_cart']

            session['count_cart'] = sum(
                [v['quant'] for v in session['products_cart'].values()])
            count_cart = session['count_cart']

            products_cart = session['products_cart']
        else:
            sum_cart = 0
            count_cart = 0
            products_cart = {}


        return HttpResponse(json.dumps({'sum_cart': sum_cart, 'count_cart':
                count_cart, 'products_cart': products_cart}))


class CartSetView(CartResultMixin):
    '''
    If quantity of product is None or  is less 0, then  this equivalent quantity equal 0
    '''
    def post(self, request, *args, **kwargs):

        if request.is_ajax:
            request.session['products_cart'] = request.session.get('products_cart', {})
            request.session['sum_cart'] = 0
            request.session['count_cart'] = 0

            product_pk = request.POST.get('product_pk', '')
            try:
                quant = int(request.POST.get('quant', '0'))
            except ValueError:
                quant = 0

            product = get_object_or_404(Product.objects, pk=product_pk)

            if quant <= 0:
                if product_pk in request.session["products_cart"]:
                    request.session["products_cart"].pop(product_pk)
            else:
                price = float(product.price_uah)
                name = product.name
                product_code = product.code
                sum_ = round(quant * price, 2)

                request.session['products_cart'][product_pk] = {
                    'product_code': product_code,
                    'name': name,
                    'price': price,
                    'quant': quant,
                    'sum_': sum_}

            return self.format_response(request.session)


class CartRemoveView(CartResultMixin):

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            product_pk = request.POST.get('product_pk', '')

            if product_pk in request.session["products_cart"]:
                request.session["products_cart"].pop(product_pk)

            return self.format_response(request.session)


class CartView(CartResultMixin):

    def get(self, request, *args, **kwargs):
        if request.is_ajax:
            return self.format_response(request.session)


    def post(self, request, *args, **kwargs):
        '''
        Clear cart
        '''
        if request.is_ajax:
            if 'products_cart' in request.session :
                request.session.pop('products_cart')
            if 'sum_cart' in request.session :
                request.session.pop('sum_cart')
            if 'count_cart' in request.session :
                request.session.pop('count_cart')

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
