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
        self.session = request.session

        if not 'cart' in self.session :
            self.session['cart'] = {'products': {}, 'total': 0, 'count': 0}
        else:
            if not 'products' in self.session['cart']:
                self.session['cart'] = {'products': {}, 'total': 0, 'count': 0}

    def _calculate(self):
        print '_calculate'
        """ Recalculate product quantity and sum """
        self.session['cart']['total'] = 0
        self.session['cart']['count'] = 0
        self.session['cart']['total'] = round(sum([v['sum_'] for v in self.session['cart']['products'].values()]), 2)
        self.session['cart']['count'] = sum([v['quant'] for v in self.session['cart']['products'].values()])


    def set(self, product_pk, quant):
        print "set"
        if quant > 0:
            product = get_object_or_404(Product, pk=product_pk)
            price = float(product.price_min)
            sum_ = round(quant * price, 2)
            product_pk = str(product_pk)
            self.session['cart']['products'][product_pk] = {'name': product.name, 'product_code': 'kjhgf', 'price': price, 'quant': quant, 'sum_': sum_}
            self._calculate()
        else:
            self.remove(product_pk)

    def remove(self, product_pk):
        print "remove", type(product_pk)
        if product_pk in self.session['cart']['products'].keys():
            print 'Yes', self.session['cart']
            print 'pop - ', product_pk, self.session['cart']['products'].pop(product_pk)
            #del self.session['cart']['products'][product_pk]
            self._calculate()
            print 'after _calculate - ', self.session['cart']

    def clear(self):
        print "clear"
        self.session['cart'] = {'products': {}, 'total': 0, 'count': 0}

    def add(self, product_pk, quant):
        print 'add'
        if product_pk in self.session['cart']['products']:
            quant += self.session['cart']['products'][product_pk]['quant']

        self.set(product_pk, quant)


class CartView(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax:
            print 'CartVew.get - request.cart-in', request.session['cart']
            '''
            cart = Cart(request)
            
            cart.clear()
            print(4556699995999)
            cart.set(2, 1)
            
            cart.set(1, 1)
            '''
            '''
            #cart.set(3, 5)
            #cart.set(4, 5)
            #cart.set(5, 5)
            '''
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
    pass
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
            cart.set(product_pk, quant)
        
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
        session = self.request.session
        '''
        if not 'products' in self.request.session:
            session['products'] = {}
            session['total'] = 0
            session['count'] = 0
        '''


        return {'summ': session['cart']['total'], 'quant': session['cart']['count']}


class ThankView(TemplateView):
    template_name = 'thank.html'
