# coding: utf-8
from __future__ import unicode_literals

from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel


@python_2_unicode_compatible
class Category(models.Model):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    name = models.CharField(_('Category name'), max_length=127)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Subcategory(models.Model):
    class Meta:
        verbose_name = _('Subcategory')
        verbose_name_plural = _('Subcategories')

    name = models.CharField(_('Subcategory name'), max_length=127)
    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name='subcategories')

    def __str__(self):
        return '{}-{}'.format(self.category, self.name)


@python_2_unicode_compatible
class Product(TimeStampedModel):
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    name = models.CharField(_('Product name'), max_length=255)
    slug = models.SlugField(
        _('Product slug'), max_length=255,
        help_text=_('This field will be shown in product URL (for SEO). It will be filled automatically.'))
    code = models.CharField(_('Product code'), max_length=127, unique=True)
    subcategory = models.ForeignKey(
        Subcategory, verbose_name=_('Product subcategory'), related_name='products')

    price_uah = models.DecimalField(
        _('Product price in UAH'), default=Decimal(0), max_digits=8, decimal_places=2)
    price_usd = models.DecimalField(
        _('Product price in USD'), default=Decimal(0), max_digits=8, decimal_places=2)
    price_eur = models.DecimalField(
        _('Product price in EUR'), default=Decimal(0), max_digits=8, decimal_places=2)

    short_description = models.CharField(
        _('Product short description'), max_length=1023, blank=True,
        help_text=_('This description will be shown on page with products list'))
    description = models.TextField(_('Product description'), blank=True)

    is_active = models.BooleanField(_('Is product active'), default=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.code)


@python_2_unicode_compatible
class ProductAttribute(models.Model):
    class Meta:
        verbose_name = _('Product attribute')
        verbose_name_plural = _('Product attributes')

    product = models.ForeignKey(Product, related_name='attributes')
    name = models.CharField(_('Attribute name'), max_length=63)
    value = models.CharField(_('Attribute value'), max_length=31)

    def __str__(self):
        return 'Attribute {}'.format(self.name)


class ProductImage(models.Model):
    class Meta:
        verbose_name = _('Product image')
        verbose_name_plural = _('Product images')

    product = models.ForeignKey(Product, related_name='images')
    image = models.ImageField(upload_to='products/', verbose_name=_('Image'))
    description = models.CharField(_('Image description'), max_length=127)
