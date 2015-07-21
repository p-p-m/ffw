#  -*- coding: utf-8 -*-

import json

from django.db.models import get_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator

from .models import TestProduct
import settings


class CSRFProtectMixin():

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(CSRFProtectMixin, self).dispatch(*args, **kwargs)


class CartClearMixin():

    def cart_clear(self, session):
        if 'products_cart' in session:
            del session['products_cart']
        if 'sum_cart' in session:
            del session['sum_cart']
        if 'count_cart' in session:
            del session['count_cart']


class CartResultView(View, CSRFProtectMixin, CartClearMixin):

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


class CartTestView(TemplateView):
    """
    For test
    """

    template_name = 'cart_test.html'

    def get_context_data(self, **kwargs):
        name_list = ('Утюг', 'Самовар', 'Холодильник', 'Пылесос', 'Фонарь')
        code_list = ('УлшН7', 'Сбор3ю4', 'Х99г7', 'ПкеН6', 'Ф342ц')
        price_list = (100.50, 300.00, 1000.00, 700.00, 93.00)
        TestProduct.objects.all().delete()

        k = 1
        while k <= 5:
            TestProduct.objects.create(pk=k, name=name_list[k-1], price_uah=price_list[k-1], code=code_list[k-1])
            k += 1

        context = super(CartTestView, self).get_context_data(**kwargs)
        context['products'] = TestProduct.objects.all()
        return context


class CartSetView(CartResultView):
    """
    Super for CartAddView
    """
    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            session = request.session
            session['products_cart'] = session.get('products_cart', {})

            product_pk = request.POST.get('product_pk', '')
            test = request.POST.get("test", False)
            try:
                quant = int(request.POST.get('quant', '0'))
            except ValueError:
                quant = 0

            if test:
                app_name = 'cart'
                model_name = 'TestProduct'
                price_field_name = 'price_uah'
                code_field_name = 'code'
                name_field_name = 'name'
            else:
                cart_settings = settings.CART_SETTINGS
                app_name = cart_settings['app_name']
                model_name = cart_settings['model_name']
                price_field_name = cart_settings['price_field_name']
                code_field_name = cart_settings['code_field_name']
                name_field_name = cart_settings['name_field_name']

            if quant <= 0:
                if product_pk in session["products_cart"]:
                    self.change_session(session["products_cart"], product_pk)
            else:
                model_product = get_model(app_name, model_name)
                product = get_object_or_404(model_product.objects, pk=product_pk)
                price = float(self.get_object_attribute(price_field_name, product))
                name = self.get_object_attribute(name_field_name, product)
                product_code = self.get_object_attribute(code_field_name, product)

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
