#  -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import View, TemplateView, FormView

from .forms import OrderForm
from .models import Cart, OrderedProduct, Order
from products.models import ProductConfiguration


# XXX: Cart endpoints completely breaks REST architecture. We need to rewrite them.
class CartMixin(object):

    def dispatch(self, request, *args, **kwargs):
        self.cart = request.session.get('cart', {'products': {}, 'total': 0, 'count': 0})
        return super(CartMixin, self).dispatch(request, *args, **kwargs)

    def format_response(self, request):
        request.session['cart'] = self.cart
        return HttpResponse(json.dumps({'cart': request.session['cart']}))


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax:
            return self.format_response(request)

    def post(self, request, *args, **kwargs):
        """ Clear cart """
        if request.is_ajax:
            self.cart ={'products': {}, 'total': 0, 'count': 0}
            return self.format_response(request)


class CartRemoveView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            product_pk_list = json.loads(request.POST.get('product_pk_list', '[]'))
            for product_pk in product_pk_list:
                Cart(self.cart).remove(product_pk)
            return self.format_response(request)


class CartSetView(CartMixin, View):

    def _call_cart(self, product_pk, quant):
        Cart(self.cart).set(product_pk, quant)

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            product_dict = json.loads(request.POST.get('product_dict', '{}'))
            for item in product_dict.items():
                self._call_cart(product_pk=item[0], quant=int(item[1]))
            return self.format_response(request)


class CartAddView(CartSetView):
    def _call_cart(self, product_pk, quant):
        Cart(self.cart).add(product_pk, quant)


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
            product = ProductConfiguration.objects.get(id=int(key))
            ordered_product = OrderedProduct(
                order=order,
                product=product,
                name=product.product.name,
                code=product.code,
                price=product.price_uah,
                quant=value['quant'],
                total=round(product.price_uah * value['quant'], 2))
            ordered_product.save()
            self.total += ordered_product.total
            self.count += ordered_product.quant

        order.count = self.count
        order.total = self.total
        order.save()
        return super(OrderView, self).form_valid(form)


class ThankView(TemplateView):
    template_name = 'thank.html'
    def get(self, request, *args, **kwargs):
        print 'in'
        for order in Order.objects.all():
            print order
            for product in OrderedProduct.objects.filter(order=order):
                print "    " , product
        return super(ThankView,self).get(self, request, *args, **kwargs)
