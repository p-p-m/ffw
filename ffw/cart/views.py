#  -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View, TemplateView, FormView
from django.utils.decorators import method_decorator

from forms import OrderForm
from models import OrderedProduct
from products.models import Product
from . import settings


class CartClearMixin():

    def cart_clear(self, session):
        if 'products_cart' in session:
            del session['products_cart']
        if 'sum_cart' in session:
            del session['sum_cart']
        if 'count_cart' in session:
            del session['count_cart']


class CartResultView(CartClearMixin, View):

    def format_response(self, session):
        if 'products_cart' in session:
            if session["products_cart"] == {}:
                self.cart_clear(session)
                sum_cart = 0
                count_cart = 0
                products_cart = {}
            else:
                session['sum_cart'] = round(sum(
                    [v['sum_'] for v in session['products_cart'].values()]), 2)
                session['count_cart'] = sum(
                    [v['quant'] for v in session['products_cart'].values()])

                count_cart = session['count_cart']
                sum_cart = session['sum_cart']
                products_cart = session['products_cart']
        else:
            self.cart_clear(session)
            sum_cart = 0
            count_cart = 0
            products_cart = {}
        return HttpResponse(
            json.dumps({'sum_cart': sum_cart, 'count_cart': count_cart, 'products_cart': products_cart}))


class CartRemoveView(CartResultView):

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            product_pk = request.POST.get('product_pk', '')

            if product_pk in request.session["products_cart"]:
                del request.session["products_cart"][product_pk]

            return self.format_response(request.session)


class CartView(CartResultView, CartClearMixin):

    def get(self, request, *args, **kwargs):
        if request.is_ajax:
            return self.format_response(request.session)

    def post(self, request, *args, **kwargs):
        """
        Clear cart
        """
        if request.is_ajax:
            self.cart_clear(request.session)

            return self.format_response(request.session)


class CartSetView(CartResultView):
    """
    Super for CartAddView
    """
    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            session = request.session
            session['products_cart'] = session.get('products_cart', {})

            product_pk = request.POST.get('product_pk', '')

            try:
                quant = int(request.POST.get('quant', '0'))
            except ValueError:
                quant = 0


            if quant <= 0:
                if product_pk in session["products_cart"]:
                    self.change_session(session["products_cart"], product_pk)
            else:
                product = get_object_or_404(Product, pk=product_pk)
                price = float(product.price_min)
                name = product.name
                product_code = 'kjhgf' #product.code

                quant = self.calc_quant(session, product_pk, quant)
                sum_ = round(quant * price, 2)

                session['products_cart'][product_pk] = {
                    'product_code': product_code,
                    'name': name,
                    'price': price,
                    'quant': quant,
                    'sum_': sum_}

        return self.format_response(session)

    def get_object_attribute(self, field_name, obj):
        return reduce(getattr, field_name.split("."), obj)

    def change_session(self, products_cart, product_pk):
        products_cart.pop(product_pk)

    def calc_quant(self, session, product_pk, quant):
        return quant


class CartAddView(CartSetView):

    def change_session(self, products_cart, product_pk):
        pass

    def calc_quant(self, session, product_pk, quant):
        if product_pk in session["products_cart"]:
            quant += session["products_cart"][product_pk]['quant']
        return quant

from models import Order


class OrderView(FormView):
    template_name = 'order.html'
    form_class = OrderForm
    success_url = 'thank/'


    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['products_cart'] = self.request.session.get('products_cart',{})
        context['count_cart'] = self.request.session.get('count_cart',0)
        context['sum_cart'] = self.request.session.get('sum_cart',0)
        return context

    def form_valid(self, form):
        order_obj = form.save()

        if 'products_cart' in self.request.session:
            for key, value in self.request.session['products_cart'].items():
                product_obj = Product.objects.get(id=int(key))
                ordered_product = OrderedProduct(
                    order=order_obj,
                    product=product_obj,
                    name=value['name'],
                    price=value['price'],
                    quant=value['quant'],
                    summ=value['sum_'])
        else:
            self.request.session['products_cart'] = {}
            self.request.session['sum_'] = 0
            self.request.session['quant'] = 0

        return super(OrderView, self).form_valid(form)


class ThankView(TemplateView):
    template_name = 'thank.html'
