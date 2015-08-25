#  -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import View, TemplateView, FormView

from .forms import OrderForm
from .models import Cart, OrderedProduct
from products.models import ProductConfiguration


# XXX: Cart endpoints completely breaks REST architecture. We need to rewrite them.
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
        #self.request.session['cart'] = cart.cart


class OrderView(FormView):
    template_name = 'order.html'
    form_class = OrderForm

    def get_success_url(self):
        return reverse('thank')

    def __init__(self):
        super(OrderView, self).__init__()
        self.success_url = self.get_success_url()

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        order = form.save()
        self.count = 0
        self.total = 0

        for key, value in self.request.session['cart']['products'].items():
            product_obj = ProductConfiguration.objects.get(id=int(key))
            ordered_product = OrderedProduct(
                order=order,
                product=product_obj,
                name=product_obj.product.name,
                price=product_obj.price_uah,
                quant=value['quant'],
                total=round(product_obj.price_uah * value['quant'], 2))
            ordered_product.save()
            self.total += ordered_product.total
            self.count += ordered_product.quant

        order.count = self.count
        order.total = self.total
        order.save()
        return super(OrderView, self).form_valid(form)


class ThankView(TemplateView):
    template_name = 'thank.html'
