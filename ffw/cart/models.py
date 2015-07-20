# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from . import settings

from get_model(settings.CART_SETTINGS['app_name'] import settings.CART_SETTINGS['model_name'])


class TestProduct(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=127, unique=True)
    price_uah = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)


class Order(models.Model):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    name = models.CharField(_('Name'), max_length=255)
    email = models.EmailField(_('E-mail'), max_length=125)
    add_communication = models.CharField(_('Additional communication'), max_length=255)


class OrderedProduct(models.Model):
    class Meta:
        verbose_name = _('Ordered products')
        verbose_name_plural = _('Ordered products')

    order = models.ForeignKey(Order, verbose_name='Order', related_name='products')
    product = models.ForeignKey(self.model_product, verbose_name='Product', related_name='ordered_product')
    price = models.FloatField(_('Price'))
 
    def get_product_model(self):
        cart_settings = settings.CART_SETTINGS
        app_name = cart_settings['app_name']
        model_name = cart_settings['model_name']
        model_product = get_model(app_name, model_name)
        return model_product

    def __init__(self):
       cart_settings = settings.CART_SETTINGS
        app_name = cart_settings['app_name']
        model_name = cart_settings['model_name']
        self. model_product = get_model(app_name, model_name)