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


class CartSet(View, CSRFProtectMixin):

    def post(self, request, *args, **kwargs):

        if request.is_ajax:
            request.session['products_cart'] = request.session.get('products_cart', {})
            request.session['sum_cart'] = 0
            request.session['count_cart'] = 0

            product_pk = request.POST.get('product_pk', '')
            quant = int(request.POST.get('quant', 0))

            product = get_object_or_404(Product.objects, pk=product_pk)
            price = float(product.price_uah)
            name = product.name
            product_code = product.code

            count = request.session['products_cart'].get(product_pk, {}).get('count', 0) + quant
            sum_ = round(count * price, 2)

            request.session['products_cart'][product_pk] = {
                'product_code': product_code,
                'name': name,
                'price': price,
                'count': count,
                'sum_': sum_}

            result(request)

            return HttpResponse(json.dumps({'sum_cart': request.session['sum_cart'], 'count_cart': (
                request.session['count_cart']), 'products_cart': request.session['products_cart']}))


class CartRemove(View, CSRFProtectMixin):

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            product_pk = request.POST.get('product_pk', '')
            del request.session["products_cart"][product_pk]
            result(request)

            return HttpResponse(json.dumps({'sum_cart': request.session['sum_cart'], 'count_cart': (
                 request.session['count_cart']),  'products_cart': request.session['products_cart']}))


class Cart(View, CSRFProtectMixin):

    def get(self,request, *args, **kwargs):
        if request.is_ajax:
            return HttpResponse(json.dumps({'sum_cart': request.session['sum_cart'], 'count_cart': (
                 request.session['count_cart']),  'products_cart': request.session['products_cart']}))

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            request.session['products_cart'] = {}
            request.session['sum_cart'] = 0
            request.session['count_cart'] = 0
            return HttpResponse(json.dumps({'sum_cart': request.session['sum_cart'], 'count_cart': (
                 request.session['count_cart']),  'products_cart': request.session['products_cart']}))


def result(request):

    request.session['sum_cart'] = round(sum(
        [v['sum_'] for v in request.session['products_cart'].values()]), 2)
    request.session['count_cart'] = sum(
        [v['count'] for v in request.session['products_cart'].values()])

