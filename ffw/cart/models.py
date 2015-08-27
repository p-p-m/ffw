# coding: utf-8
from __future__ import unicode_literals

import json
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from .exceptions import CartException
from products.models import ProductConfiguration


class Order(TimeStampedModel):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    name = models.CharField(_('Name'), max_length=255)
    email = models.EmailField(_('E-mail'), max_length=125)
    phone = models.CharField(_('Phone'), max_length=125)
    contacts = models.CharField(_('Additional communication'), max_length=255, blank=True)
    total = models.DecimalField(_('Total'), decimal_places=2, max_digits=9, default=0)
    count = models.IntegerField(_('Quantity'), default=0)

    def __str__(self):
        return  str(self.pk) + " " + self.name + " " + str(self.count) + " " + str(self.total)

class OrderedProduct(models.Model):
    class Meta:
        verbose_name = _('Ordered products')
        verbose_name_plural = _('Ordered products')

    order = models.ForeignKey(Order, verbose_name='Order', related_name='products')
    # XXX: This FK provides circular dependency in applications cart and products. We need to use abstract product
    # from cart settings
    product = models.ForeignKey(ProductConfiguration, verbose_name='Product', related_name='ordered_product')
    name = models.CharField(_('Name'), max_length=127)
    code = models.CharField(_('Code'), max_length=127)
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=7)
    quant = models.IntegerField(_('Quantity'), default=0)
    total = models.DecimalField(_('Total'), decimal_places=2, max_digits=9)

    def __str__(self):
        return str(self.pk) + " " + self.name + " " + self.product.code + " " + str(self.price) + " " + str(self.quant) + " " + str(self.total)


class CartProduct(object):
    """ Wrapper for abstract product that is defined by cart application settings """
    # TODO: rewrite this class to use product table configuration from cart settings
    def __init__(self, product_pk):
        product_pk = int(product_pk)

        try:
            self.product = ProductConfiguration.objects.get(pk=product_pk)
        except ProductConfiguration.DoesNotExist:
            raise CartException("Can not find product with pk {}".format(product_pk))

    @property
    def name(self):
        return self.product.product.name

    @property
    def code(self):
        return self.product.code

    @property
    def price(self):
        return self.product.price_uah

    @property
    def pk_int(self):
        return self.product.pk

    @property
    def pk_str(self):
        return str(self.product.pk).strip()


class Cart(object):

    def __init__(self, cart):
        self.cart = cart

    def _calculate(self):
        """ Recalculate product quantity and sum """
        self.cart['total'] = float(round(sum([v['sum_'] for v in self.cart['products'].values()]), 2))
        self.cart['count'] = sum([v['quant'] for v in self.cart['products'].values()])

    def set(self, product_pk, quant):
        if quant > 0:
            product = CartProduct(product_pk)

            self.cart['products'][product_pk] = {
                'name': product.name,
                'product_code': product.code,
                'price': float(product.price),
                'quant': quant,
                'sum_': float(quant * product.price),
            }
            self._calculate()
        else:
            self.remove(product_pk)

    def remove(self, product_pk):
        product = CartProduct(product_pk)
        try:
            del self.cart['products'][product.pk_str]
        except KeyError:
            raise CartException('Cart does not contain product with key {}'.format(product.pk_str))
        self._calculate()

    def add(self, product_pk, quant):
        if str(product_pk).strip()  in self.cart['products']:
            quant += self.cart['products'][str(product_pk).strip()]['quant']

        self.set(product_pk, quant)
