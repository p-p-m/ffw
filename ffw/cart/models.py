# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from . import settings



from get_model(settings.CART_SETTINGS['app_name'] import settings.CART_SETTINGS['model_name'])


class TestProduct(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=127, unique=True)
    price_uah = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)


class Order(TimeStampedModel):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    name = models.CharField(_('Name'), max_length=255)
    email = models.EmailField(_('E-mail'), max_length=125)
    add_communication = models.CharField(_('Additional communication'), max_length=255, blank=True)
    total = models.DecimalField(_('Total'), decimal_places=2, max_digits=9)



def get_product_model_str():
        cart_settings = settings.CART_SETTINGS
        app_name = cart_settings['app_name']
        model_name = cart_settings['model_name']
        model_product =app_name + '.' + model_name
        return model_product


class OrderedProduct(models.Model):
    class Meta:
        verbose_name = _('Ordered products')
        verbose_name_plural = _('Ordered products')


    order = models.ForeignKey(Order, verbose_name='Order', related_name='products')
    product = models.ForeignKey(get_model(settings.CART_SETTINGS['app_name'], settings.CART_SETTINGS['model_name']), 
        verbose_name='Product', related_name='ordered_product')
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=7)
    quantity = models.IntegerField(_('Quantity'))
    sum = models.DecimalField(_('Sum'), decimal_places=2, max_digits=9)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            'name',
            'email',
            'add_communication',
            'total']
        
    order = models.ForeignKey(Order, verbose_name='Order', related_name='products')
    product = models.ForeignKey(get_product_model(), verbose_name='Product', related_name='ordered_product')
    price = models.FloatField(_('Price'))

