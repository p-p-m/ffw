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
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator


class CartSet(TemplateView):

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
         return super(CartSet, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):

        if request.is_ajax:
            cont = cont_get(request)

            request.session['products_cart'] = request.session.get('products_cart', {})
            request.session['sum_cart'] = 0
            request.session['count_cart'] = 0

            product_pk = request.POST.get('product_pk', '')
            quant = int(request.POST.get('quant', 0))

            product = get_object_or_404(Product.objects, pk=product_pk)
            price = float(product.price_uah)
            name = product.name
            product_code = product.code

            count = 0
            if product_pk in request.session['products_cart'].keys():
                count = request.session['products_cart'][product_pk].get('count',0)

            count += quant
            sum_ = round(count * price, 2)

            request.session['products_cart'][product_pk] = {
                'product_code': product_code,
                'name': name,
                'price': price,
                'count': count,
                'sum_': sum_}

            result(request)

            return HttpResponse(json.dumps({'sum_cart': request.session['sum_cart'], 'count_cart': (
                request.session['count_cart']), 'products_cart': request.session['products_cart']}), cont)


class CartRemove(TemplateView):

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
         return super(CartRemove, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            cont = cont_get(request)

            product_pk = request.POST.get('product_pk', '')
            request.session["products_cart"].pop(product_pk)
            result(request)

            return HttpResponse(json.dumps({'sum_cart': request.session['sum_cart'], 'count_cart': (
                 request.session['count_cart']),  'products_cart': request.session['products_cart']}), cont)


class Cart(TemplateView):

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(Cart, self).dispatch(*args, **kwargs)

    def get(self,request, *args, **kwargs):
        if request.is_ajax:
            return HttpResponse(json.dumps({'sum_cart': request.session['sum_cart'], 'count_cart': (
                 request.session['count_cart']),  'products_cart': request.session['products_cart']}))

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            cont = cont_get(request)
            request.session['products_cart'] = {}
            request.session['sum_cart'] = 0
            request.session['count_cart'] = 0
            return HttpResponse(json.dumps({'sum_cart': request.session['sum_cart'], 'count_cart': (
                 request.session['count_cart']),  'products_cart': request.session['products_cart']}), cont)


def result(request):

    request.session['sum_cart'] = round(sum(
        [v['sum_'] for v in request.session['products_cart'].values()]), 2)
    request.session['count_cart'] = sum(
        [v['count'] for v in request.session['products_cart'].values()])


def cont_get(request):

    cont = {}
    cont.update(csrf(request))
    return cont
