#  -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View, TemplateView, FormView
from django.views.generic.base import ContextMixin
from django.utils.decorators import method_decorator

from .forms import OrderForm
from .models import OrderedProduct
from products.models import Product, ProductConfiguration


class Cart(object):

    def __init__(self, request):
        if not 'cart' in request.session :
            request.session['cart'] = {'products': {}, 'total': 0, 'count': 0}
        else:
            if not 'products' in request.session['cart']:
                request.session['cart'] = {'products': {}, 'total': 0, 'count': 0}

        self.cart = request.session['cart']

    def _calculate(self):
        """ Recalculate product quantity and sum """
        self.cart['total'] = round(sum([v['sum_'] for v in self.cart['products'].values()]), 2)
        self.cart['count'] = sum([v['quant'] for v in self.cart['products'].values()])

    def set(self, product_pk, quant):
        if quant > 0:
            product_pk = int(product_pk)
            product = get_object_or_404(ProductConfiguration, pk=product_pk)
            price = float(product.price_uah)
            product_code = product.code
            name = product.product.name
            sum_ = round(quant * price, 2)
            product_pk = str(product_pk)
            self.cart['products'][product_pk] = {'name': name, 'product_code': product_code, 'price': price,
                                                                  'quant': quant, 'sum_': sum_}
            self._calculate()
        else:
            self.remove(product_pk)

    def remove(self, product_pk):
        product_pk = str(product_pk)
        if product_pk in self.cart['products'].keys():
            del self.cart['products'][product_pk]
            self._calculate()

    def clear(self):
        self.cart = {'products': {}, 'total': 0, 'count': 0}

    def add(self, product_pk, quant):
        product_pk = str(product_pk)
        if product_pk in self.cart['products']:
            quant += self.cart['products'][product_pk]['quant']

        self.set(product_pk, quant)

class ResponseView(View):
    def format_response(self, cart):
        self.request.session['cart'] = cart.cart
        return HttpResponse(json.dumps({'cart': self.request.session['cart']}))


class CartView(ResponseView):

    def get(self, request, *args, **kwargs):
        if request.is_ajax:
            cart = Cart(request)
            return self.format_response(cart)

    def post(self, request, *args, **kwargs):
        """ Clear cart """
        if request.is_ajax:
            cart = Cart(request)
            cart.clear()
            return self.format_response(cart)


class CartRemoveView(ResponseView):

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            product_pk = request.POST.get('product_pk', '')
            cart = Cart(request)
            cart.remove(product_pk)
            return self.format_response(cart)


class CartSetView(ResponseView):

    def _call_cart(self, cart, product_pk, quant):
        cart.set(product_pk, quant)

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            product_pk = request.POST.get('product_pk', '')

            try:
                quant = int(request.POST.get('quant', '0'))
            except ValueError:
                quant = 0

            cart = Cart(request)
            self._call_cart(cart, product_pk, quant)
            return self.format_response(cart)


class CartAddView(CartSetView):
    def _call_cart(self, cart, product_pk, quant):
        cart.add(product_pk, quant)
        self.request.session['cart'] = cart.cart


class OrderView(FormView):
    template_name = 'order.html'
    form_class = OrderForm
    success_url = 'thank/'
    #success_url = reverse('thank')

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        order_obj = form.save()

        for key, value in self.request.session['cart']['products'].items():
            product_obj = Product.objects.get(id=int(key))
            ordered_product = OrderedProduct(
                order=order_obj,
                product=product_obj,
                name=value['name'],
                price=value['price'],
                quant=value['quant'],
                summ=value['sum_'])

        return super(OrderView, self).form_valid(form)

    def get_initial(self):
        if not 'cart' in self.request.session :
            self.request.session['cart'] = {'products': {}, 'total': 0, 'count': 0}
        else:
            if not 'products' in self.request.session['cart']:
                self.request.session['cart'] = {'products': {}, 'total': 0, 'count': 0}

        return {'total': self.request.session['cart']['total'], 'quant': self.request.session['cart']['count']}

class ThankView(TemplateView):
    template_name = 'thank.html'
