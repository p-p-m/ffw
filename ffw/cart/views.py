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


@csrf_protect
def add(request, *args, **kwargs):
    if request.is_ajax:
        if request.method == 'POST':
            c = {}
            c.update(csrf(request))

            request.session['products'] = request.session.get('products', {})
            request.session['sum_cart'] = 0
            request.session['count_cart'] = 0
 
            product_pk = request.POST.get('product_pk', '')
            quant = int(request.POST.get('quant', 0))

            product = get_object_or_404(Product.objects, pk=product_pk)
            price = float(product.price_uah)
            name = product.name
            product_code = product.code
            count = request.session['products'][product_pk].get('count',0)
            print(count, quant)
            count += quant
            sum_ = count * price
            print(count, quant,sum_,product_pk)
            status = 'added'
            request.session['products'][product_pk] = {
                'product_code': product_code,
                'name': name,
                'price': price,
                'count': count,
                'sum': sum_}

            print(request.session['products'][product_pk]) 
            request.session['sum_cart'] = sum(
                [v['sum'] for v in request.session['products'].values()])
            request.session['count_cart'] = len(request.session['products'])

            return HttpResponse(json.dumps({'sum_cart': request.session['sum_cart'], 'count_cart': (
                request.session['count_cart']), 'status': status}), c)


@csrf_protect
def cart(request, *args, **kwargs):

    if request.is_ajax:
        if request.method == 'POST':
            c = {}
            c.update(csrf(request))

            #  Data of cart in session: {'sum_cart': ..., 'count_cart': ..., 'products': {pk1: {'product_code': ..., 'name': ...,
            #  'price': ...}, pk2: {'product_code': ...,'name': ..., 'price': ...}, ....}}.
            action = request.POST.get('action', '')
            request.session['products'] = request.session.get('products', {})
            request.session['sum_cart'] = 0
            request.session['count_cart'] = 0

            #  Action can be: 1 - "remove", 2 - 'clear', 3 - "add" (or any name includiing '' - its equal '"add").
            # Status can be: "added", "removed", "exist", "cleared"
            if action == 'clear':
                request.session['products'] = {}
                status = 'cleared'
                return

            # Action is 'remove' or 'add'
            product_pk = request.POST.get('product_pk', '')
            product = get_object_or_404(Product.objects, pk=product_pk)
            price = float(product.price_uah)
            name = product.name
            product_code = product.code

            if action == 'remove':
                del request.session['products'][product_pk]
                status = 'remove'
            else:

                # Action is 'add'
                if product_pk in request.session['products'].keys():
                    status = 'exist'
                else:
                    status = 'added'
                    request.session['products'][product_pk] = {
                        'product_code': product_code,
                        'name': name,
                        'price': price}

            request.session['sum_cart'] = sum(
                [v['price'] for v in request.session['products'].values()])
            request.session['count_cart'] = len(request.session['products'])

            return HttpResponse(json.dumps({'sum_cart': request.session['sum_cart'], 'count_cart': (
                request.session['count_cart']), 'status': status}), c)
