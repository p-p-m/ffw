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
from django.views.generic import View
from django.utils.decorators import method_decorator


class CSRFProtectMixin():
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
         return super(CartSet, self).dispatch(*args, **kwargs)

class CartResult(View, CSRFProtectMixin):

    def format_response(self, session):
        session['sum_cart'] = round(sum(
            [v['sum_'] for v in session['products_cart'].values()]), 2)
        session['count_cart'] = sum(
            [v['quant'] for v in session['products_cart'].values()])

        return HttpResponse(json.dumps({'sum_cart': session['sum_cart'], 'count_cart': (
                session['count_cart']), 'products_cart': session['products_cart']}))


class CartSet(CartResult):

    def post(self, request, *args, **kwargs):

        if request.is_ajax:
            request.session['products_cart'] = request.session.get('products_cart', {})
            request.session['sum_cart'] = 0
            request.session['count_cart'] = 0

            product_pk = request.POST.get('product_pk', '')
            quant = int(request.POST.get('quant', 0))
            product = get_object_or_404(Product.objects, pk=product_pk)

            if quant == 0:
                del request.session["products_cart"][product_pk]
            elif quant > 0:
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


class CartRemove(CartResult):

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            product_pk = request.POST.get('product_pk', '')
            del request.session["products_cart"][product_pk]

            return self.format_response(request.session)

class Cart(CartResult):

    def get(self,request, *args, **kwargs):
        if request.is_ajax:
            return self.format_response(request.session)

    def post(self, request, *args, **kwargs):
        '''
        Clear cart
        '''
        if request.is_ajax:
            request.session['products_cart'] = {}
            request.session['sum_cart'] = 0
            request.session['count_cart'] = 0

            return self.format_response(request.session)
