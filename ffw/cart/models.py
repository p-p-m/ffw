# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from products.models import Product
from . import settings


class Order(TimeStampedModel):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    name = models.CharField(_('Name'), max_length=255)
    email = models.EmailField(_('E-mail'), max_length=125)
    add_communication = models.CharField(_('Additional communication'), max_length=255, blank=True)
    sum = models.DecimalField(_('Sum'), decimal_places=2, max_digits=9, default=0)
    quant = models.IntegerField(_('Quantity'),default=0)


class OrderedProduct(models.Model):
    class Meta:
        verbose_name = _('Ordered products')
        verbose_name_plural = _('Ordered products')


    order = models.ForeignKey(Order, verbose_name='Order', related_name='products')
    product = models.ForeignKey(Product, verbose_name='Product', related_name='ordered_product')
    name = models.CharField(_('Name'), max_length=127)
    code = models.CharField(_('Code'), max_length=127, unique=True)
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=7)
    quant = models.IntegerField(_('Quantity'), default=0)
    sum = models.DecimalField(_('Sum'), decimal_places=2, max_digits=9)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            'name',
            'email',
            'add_communication',
            'quant',
            'sum']
