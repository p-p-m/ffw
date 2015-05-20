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
def set( request, *args, **kwargs ):

    #product_data = product_data_get( request )
    if request.is_ajax:
        if request.method == 'POST':
            cont = cont_get(request)

            request.session[ 'products' ] = request.session.get( 'products', {})
            request.session[ 'sum_cart' ] = 0
            request.session[ 'count_cart' ] = 0

            product_pk = request.POST.get( 'product_pk', '' )
            quant = int( request.POST.get( 'quant', 0 ))

            product = get_object_or_404( Product.objects, pk=product_pk )
            price = float( product.price_uah )
            name = product.name
            product_code = product.code

            count = 0
            if product_pk in request.session[ 'products' ].keys():
                count = request.session[ 'products' ][ product_pk ].get( 'count',0 )

            count += quant
            sum_ = round( count * price, 2 )

            request.session[ 'products' ][ product_pk ] = {
                'product_code': product_code,
                'name': name,
                'price': price,
                'count': count,
                'sum_': sum_}

            result(request)

    return HttpResponse( json.dumps({ 'sum_cart': request.session[ 'sum_cart' ], 'count_cart': (
        request.session[ 'count_cart' ])}), cont )


def result( request ):
    request.session[ 'sum_cart' ] = round(sum(
        [ v[ 'sum_' ] for v in request.session[ 'products' ].values()]), 2 )
    request.session['count_cart'] = sum(
        [ v[ 'count' ] for v in request.session[ 'products' ].values()])


def cont_get( request ):
    cont = {}
    cont.update( csrf( request ))
    return cont


@csrf_protect
def remove( request, *args, **kwargs ):
    if request.is_ajax:
        if request.method == 'POST':
            cont = cont_get(request)

            product_pk = request.POST.get( 'product_pk', '' )
            request.session[ "products" ].pop( product_pk )
            result( request )

        return HttpResponse( json.dumps({ 'sum_cart': request.session[ 'sum_cart' ], 'count_cart': (
            request.session[ 'count_cart' ])}), cont )


@csrf_protect
def cart( request, *args, **kwargs ):
    if request.is_ajax:

        if request.method == 'DELETE':
            cont = cont_get(request)
            request.session[ 'products' ] = {}
            request.session[ 'sum_cart' ] = 0
            request.session[ 'count_cart' ] = 0
            return HttpResponse( json.dumps({}, cont ))

        elif request.method == 'GET':
            return HttpResponse( json.dumps({ 'products': request.session[ 'products' ],
                'sum_cart': request.session[ 'sum_cart' ], 'count_cart': request.session[ 'count_cart' ]}))