#  -*- coding: utf-8 -*-
import json


from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
#from django.views.generic import ListView, View

#import forms
import models
from django.utils.translation import ugettext_lazy as _

from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def cart(request, *args, **kwargs):
    if request.is_ajax:
        if request.method == 'POST':
            c = {}
            c.update(csrf(request))

            #  data of cart in session: {'sum_cart': ..., 'count_cart': ..., 'products': {product_code1: {'name': ...,
            #  'price': ..., product_code2: {'name': ..., 'price': ...}, ....}}
            action = request.POST.get('action', '')
            request.session['products'] = request.session.get('products', {})
            request.session['sum_cart'] = 0
            request.session['count_cart'] = 0
            # if product is in the cart, msg = 'The product alredy is in the cart', else 'the product add'
            msg = ''

            #  action can be: 1 - "remove", 2 - 'clear', 3 - "add" (or any name include '' - its equal '"add")
            if action == 'clear':
                request.session['products'] = {}
                return

            # 'remove' or 'add'
            product_pk = request.POST.get('product_pk', '')
            product = get_object_or_404(models.Product.objects, pk=product_pk)
            price = float(product.price_uah)
            name = product.name

            if action == 'remove':
                del request.session['products'][product_pk]
            else:
                # action is 'add'
                if product_pk in request.session['products'].keys():
                    msg = name + ' is in the cart already'
                else:
                    msg = name + 'add in the cart'
                    request.session['products'][product_pk] = {'name': name, 'price': price}

            request.session['sum_cart'] = sum([v['price'] for v in request.session['products'].values()])
            request.session['count_cart'] = len(request.session['products'])


            return HttpResponse(json.dumps({'sum_cart': request.session['sum_cart'], 'count_cart': (
                request.session['count_cart']), 'msg': msg}), c)
