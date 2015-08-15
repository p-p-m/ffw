#  -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View, TemplateView, FormView
from django.views.generic.base import ContextMixin
from django.utils.decorators import method_decorator

from forms import OrderForm
from models import OrderedProduct
from products.models import Product
from . import settings


class Cart():

    def __init__(self, request):

        print '__init__'
        if not 'cart' in request.session :
            print 1111111111111111111
            request.session['cart'] = {'products': {}, 'total': 0, 'count': 0}
        else:
            if not 'products' in request.session['cart']:
                print 22222222222222222222
                request.session['cart'] = {'products': {}, 'total': 0, 'count': 0}

        self.cart = request.session['cart']
        self.products = request.session['cart']['products']

    def _calculate(self):
        print '_calculate'
        """ Recalculate product quantity and sum """
        self.cart['total'] = round(sum([v['sum_'] for v in self.products.values()]), 2)
        self.cart['count'] = sum([v['quant'] for v in self.products.values()])


    def set(self, product_pk, quant):
        print "set"
        if quant > 0:
            product_pk = int(product_pk)
            product = get_object_or_404(Product, pk=product_pk)
            price = float(product.price_min)
            sum_ = round(quant * price, 2)
            product_pk = str(product_pk)
            self.products[product_pk] = {'name': product.name, 'product_code': 'kjhgf', 'price': price, 'quant': quant, 'sum_': sum_}

            self._calculate()
        else:
            self.remove(product_pk)

    def remove(self, product_pk):
        print "remove", type(product_pk)
        if product_pk in self.products.keys():
            print 'Yes', self.cart
            print 'pop - ', product_pk, self.products.pop(product_pk)
            #del self.session['cart']['products'][product_pk]
            self._calculate()
            print 'after _calculate - ', self.cart

    def clear(self):
        print "clear"
        self.cart = {'products': {}, 'total': 0, 'count': 0}

    def add(self, product_pk, quant):
        print 'add'
        if product_pk in self.session['cart']['products']:
            quant += self.session['cart']['products'][product_pk]['quant']

        self.set(product_pk, quant)


class CartView(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax:


            print 'CartVew.get - request.cart-in', request.session['cart']['count'], request.session['cart']['total'], request.session['cart']['products'].keys()
            cart = Cart(request)
            #cart.clear()



            cart.set(3, 1)

            #cart.set(2, 1)
            #cart.set(1,1)
            #cart.remove(3)
            request.session['cart'] = cart.cart
            
            print '5555555', cart.products
            request.session['cart']['products'] = cart.products
            
            print 'CartVew.get - request.cart-out', request.session['cart']['count'], request.session['cart']['total'], request.session['cart']['products'].keys()

        return HttpResponse(json.dumps({'cart': request.session['cart']}))

    def post(self, request, *args, **kwargs):
        """
        Clear cart
        """
        if request.is_ajax:
            Cart(request).clear()

            return HttpResponse(json.dumps({'cart': request.session['cart']}))


class CartRemoveView(View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            print ('cartRemoveView-in - ' , request.session['cart'])
            product_pk = request.POST.get('product_pk', '')
            cart = Cart(request)
            cart.remove(product_pk)
            print ('cartRemoveView-out - cart.cart' , cart.session['cart'])
            print ('cartRemoveView-out - request.cart' , request.session['cart'])
        return HttpResponse((json.dumps({'cart': request.session['cart']})))


class CartSetView(View):

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
            print 'CartSetVew.cart - out',  request.session['cart']
            return HttpResponse(json.dumps({'cart': request.session['cart']}))


class CartAddView(CartSetView):
    pass
    def _call_cart(self, cart, product_pk, quant):
        cart.add(product_pk, quant)


class OrderView(FormView):
    print "OrderView"
    template_name = 'order.html'
    form_class = OrderForm
    success_url = 'thank/'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['cart'] = self.request.session['cart']
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
        '''
        session = self.request.session

        if not 'products' in self.request.session:
            session['products'] = {}
            session['total'] = 0
            session['count'] = 0
        '''


        return {'summ': self.request.session['cart']['total'], 'quant': self.request.session['cart']['count']}


class ThankView(TemplateView):
    template_name = 'thank.html'
