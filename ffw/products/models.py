# coding: utf-8
from __future__ import unicode_literals

import logging

from constance import config
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField
from model_utils.models import TimeStampedModel

from . import exceptions

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Characteristic(models.Model):
    class Meta:
        verbose_name = _('Characteristic')
        verbose_name_plural = _('Characteristics')

    name = models.CharField(_('Characteristic name'), max_length=255, unique=True)
    description = models.TextField(_('Characteristic description'), blank=True)
    default_value = models.CharField(_('Default value'), max_length=127, blank=True)
    units = models.CharField(_('Units'), max_length=50, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class AbstractCategory(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(_('Name'), max_length=127)
    slug = models.CharField(
        _('Slug'), max_length=127, unique=True,
        help_text=_('This field will be shown in URL address (for SEO). It will be filled automatically.'))
    is_active = models.BooleanField(default=True)


class SectionCharacteristic(models.Model):
    section = models.ForeignKey('Section')
    characteristic = models.ForeignKey(Characteristic)


@python_2_unicode_compatible
class Section(AbstractCategory):
    characteristics = models.ManyToManyField(Characteristic, related_name='sections', through=SectionCharacteristic)

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Section')

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('products', args=(self.slug,))

    def get_categories(self):
        return self.categories.all()


class CategoryCharacteristic(models.Model):
    category = models.ForeignKey('Category')
    characteristic = models.ForeignKey(Characteristic)


@python_2_unicode_compatible
class Category(AbstractCategory):
    characteristics = models.ManyToManyField(Characteristic, related_name='categories', through=CategoryCharacteristic)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    section = models.ForeignKey(Section, verbose_name=_('Section'), related_name='categories')
    image = models.ImageField(upload_to='categories/', verbose_name=_('Image'), blank=True)

    def __str__(self):
        return '{}-{}'.format(self.section, self.name)

    def get_url(self):
        return reverse('products', args=(self.section.slug, self.slug))

    def get_subcategories(self):
        return self.subcategories.all()


class SubcategoryCharacteristic(models.Model):
    subcategory = models.ForeignKey('Subcategory')
    characteristic = models.ForeignKey(Characteristic)


@python_2_unicode_compatible
class Subcategory(AbstractCategory):
    characteristics = models.ManyToManyField(
        Characteristic, related_name='subcategories', through=SubcategoryCharacteristic)

    class Meta:
        verbose_name = _('Subcategory')
        verbose_name_plural = _('Subcategories')

    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name='subcategories')
    image = models.ImageField(upload_to='subcategories/', verbose_name=_('Image'), blank=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.category.section.name, self.category.name, self.name)

    def get_url(self):
        return reverse('products', args=(self.category.section.slug, self.category.slug, self.slug))


PRODUCT_CATEGORIES_MODELS = [Subcategory, Category, Section]


@python_2_unicode_compatible
class Product(TimeStampedModel):
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    name = models.CharField(_('Name'), max_length=255, unique=True)
    slug = models.SlugField(
        _('Slug'), max_length=255, unique=True,
        help_text=_('This field will be shown in URL address (for SEO). It will be filled automatically.'))
    short_description = models.CharField(
        _('Product short description'), max_length=1023, blank=True,
        help_text=_('This description will be shown on page with products list'))
    description = models.TextField(_('Product description'), blank=True)

    subcategory = models.ForeignKey(Subcategory, verbose_name=_('Subcategory'), related_name='products')

    is_active = models.BooleanField(_('Is product active'), default=True)
    rating = models.FloatField(
        _('Product rating'), default=4, validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_('Number between 0 and 5 that will be used for default sorting on products page. Products with '
                    'higher numbers will be displayed higher'))
    price_min = models.FloatField(_('Max price in UAH'), null=True)
    price_max = models.FloatField(_('Min price in UAH'), null=True)

    def __str__(self):
        return '{}'.format(self.name)

    def get_url(self):
        return reverse('product', args=(self.slug, ))

    def get_images(self):
        return self.images.all()

    def get_first_image(self):
        return self.images.first()

    def get_characteristics(self):
        query = (
            models.Q(categories=self.subcategory.category) |
            models.Q(subcategories=self.subcategory) |
            models.Q(sections=self.subcategory.category.section)
        )
        return Characteristic.objects.filter(query)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Product, self).save(*args, **kwargs)


@python_2_unicode_compatible
class ProductConfiguration(models.Model):
    class Meta:
        verbose_name = _('Product configuration')
        verbose_name_plural = _('Product configurations')

    product = models.ForeignKey(Product, verbose_name=_('Product'), related_name='configurations')
    code = models.CharField(_('Code'), max_length=127, unique=True)
    is_active = models.BooleanField(_('Is configuration active'), default=True)
    price_uah = models.FloatField(_('Price in UAH'), null=True)
    price_eur = models.FloatField(_('Price in EUR'), null=True)
    price_usd = models.FloatField(_('Price in USD'), null=True)

    def __str__(self):
        return '{}-{}'.format(self.product, self.code)

    def clean(self):
        if not self.price_uah and not self.price_usd and not self.price_eur:
            raise ValidationError('At least one price has to be defined')

    @property
    def attrs(self):
        """
        Shortcut for attributes

        Allow shorter access to attributes.
        Example: product_configuration.attrs.brand - will return brand attribute value
                 product_configuration.attrs.brand = 'qwe' - will send brand attribute value
        """
        class Attrs(object):
            def __getattr__(self_, key):
                return self.attributes.get(name='key').value

            def __setattr__(self_, key, value):
                attr, _ = self.attributes.get_or_create(name=key)
                attr.value = value
                attr.save()

        return Attrs()

    def init_prices(self):
        if self.price_uah:
            value = float(self.price_uah)
        elif self.price_usd:
            value = float(self.price_usd) * config.USD_RATE
        elif self.price_eur:
            value = float(self.price_eur) * config.EUR_RATE

        if not self.price_uah:
            self.price_uah = value
        if not self.price_usd:
            self.price_usd = value / config.USD_RATE
        if not self.price_eur:
            self.price_eur = value / config.EUR_RATE

    def save(self, *args, **kwargs):
        self.init_prices()
        super(ProductConfiguration, self).save(*args, **kwargs)


@python_2_unicode_compatible
class ProductAttribute(models.Model):
    class Meta:
        verbose_name = _('Product attribute')
        verbose_name_plural = _('Product attributes')

    characteristic = models.ForeignKey(Characteristic, related_name='attributes', null=True)
    product_configuration = models.ForeignKey(ProductConfiguration, related_name='attributes')
    name = models.CharField(_('Name'), max_length=63)
    value = models.CharField(_('Value'), max_length=31)
    value_float = models.FloatField(
        _('Attribute value as number'), blank=True, null=True,
        help_text=_('This field will be defined automatically'))
    units = models.CharField(_('Units'), max_length=50, blank=True)

    def __str__(self):
        return 'Attribute {}'.format(self.name)

    def _init_values(self):
        try:
            self.value_float = float(self.value)
        except (ValueError, TypeError):
            self.value_float = None

    def save(self, *args, **kwargs):
        self._init_values()
        return super(ProductAttribute, self).save(*args, **kwargs)


class ProductImage(models.Model):
    class Meta:
        verbose_name = _('Product image')
        verbose_name_plural = _('Product images')

    product = models.ForeignKey(Product, related_name='images')
    image = models.ImageField(upload_to='products/', verbose_name=_('Image'))
    description = models.CharField(_('Image description'), max_length=127, blank=True)


# # XXX: Filter will be moved to separate application
# @python_2_unicode_compatible
# class ProductFilter(models.Model):
#     class Meta:
#         verbose_name = _('Product filter')
#         verbose_name_plural = _('Product filters')

#     TYPES = (
#         ('NUMERIC', _('Numeric filter')),
#         ('CHOICES', _('Choices filter')),
#         ('NUMERIC_RANGES', _('Intervals filter')),
#     )

#     subcategory = models.ForeignKey(Subcategory, related_name='product_filters', blank=True, null=True)
#     category = models.ForeignKey(Category, related_name='product_filters', blank=True, null=True)
#     attribute_name = models.CharField(_('Attribute name'), max_length=63)
#     name = models.CharField(_('Filter displayed name'), max_length=63)
#     filter_type = models.CharField(max_length=15, choices=TYPES)
#     ranges_count = models.SmallIntegerField(
#         _('Amount of ranges'),
#         default=5, validators=[MinValueValidator(2), MaxValueValidator(50)], null=True,
#         help_text=_('This field is necessary only for interval filters'),
#     )
#     values = JSONField(
#         _('Filter values'), help_text=_('Internal filter values. DO NOT modify them.'), default={}, blank=True)

#     def __str__(self):
#         return '{} filter for {} {}'.format(self.filter_type, self.category, self.subcategory)

#     def _update_numeric_filter(self, attributes):
#         max_value = self.values.get('max', float('-inf'))
#         min_value = self.values.get('min', float('inf'))
#         for attribute in attributes:
#             try:
#                 attribute_value = float(attribute.value)
#             except ValueError:
#                 logger.warning('Cannot update filter with %s value for product %s', attribute.value, self.product)
#                 raise exceptions.ProductFilterUpdateException(
#                     _('Cannot update filter with %s value for product %s' % attribute.value, self.product))
#             max_value = max(max_value, attribute_value)
#             min_value = min(min_value, attribute_value)

#         self.values['max'] = max_value
#         self.values['min'] = min_value

#     def _update_choices_filter(self, attributes):
#         choices = self.values.get('choices', [])
#         for attribute in attributes:
#             attribute_value = str(attribute.value)
#             if attribute_value.lower() not in choices:
#                 choices.append(attribute_value.lower())
#         self.values['choices'] = choices

#     def _update_numeric_ranges_filter_ranges(self, attributes):
#         self._update_numeric_filter(attributes)
#         if attributes and 'ranges' not in self.values:
#             try:
#                 max_value = self.values['max']
#                 min_value = self.values['min']
#             except KeyError:
#                 logger.warning('Cannot set ranges for filter %s - min or max value is not set', self.id)
#                 raise exceptions.ProductFilterUpdateException(
#                     _('Cannot set ranges for filter - min or max is not set'))
#             interval = float(max_value - min_value) / self.ranges_count
#             self.values['ranges'] = [
#                 (min_value + i * interval, min_value + (i + 1) * interval) for i in range(self.ranges_count)]
#             self.values['ranges'].append((min_value + (self.ranges_count - 1) * interval, max_value))

#     def _update_numeric_ranges_filter(self, attributes):
#         self._update_numeric_filter(attributes)
#         self._update_filter_ranges(attributes)

#     def get_related_attributes(self):
#         if self.category:
#             return ProductAttribute.objects.filter(
#                 name=self.attribute_name, product__subcategory__category=self.category)
#         else:
#             return ProductAttribute.objects.filter(
#                 name=self.attribute_name, product__subcategory=self.subcategory)

#     def update(self, attributes):
#         if self.filter_type == 'NUMERIC':
#             self._update_numeric_filter(attributes)
#         elif self.filter_type == 'CHOICES':
#             self._update_choices_filter(attributes)
#         elif self.filter_type == 'NUMERIC_RANGES':
#             self._update_numeric_ranges_filter_ranges(attributes)

#     def clean(self):
#         if self.subcategory is None and self.category is None:
#             raise ValidationError(_('Product filter have to belong to category, subcategory or both'))

#         attributes = self.get_related_attributes()
#         try:
#             self.update(attributes)
#         except exceptions.ProductFilterException as e:
#             raise ValidationError(e.message)

#     def get_numeric_filtered_attributes(self, min_value, max_value):
#         if self.filter_type != 'NUMERIC':
#             raise exceptions.ProductFilterFilterException('Wrong filter function')
#         attributes = self.get_related_attributes()
#         if min_value is not None:
#             attributes = attributes.filter(value_float__gte=min_value)
#         if max_value is not None:
#             attributes = attributes.filter(value_float__lte=max_value)
#         return attributes

#     def get_choices_filtered_attributes(self, selected_values):
#         if self.filter_type != 'CHOICES':
#             raise exceptions.ProductFilterFilterException('Wrong filter function')
#         attributes = self.get_related_attributes()
#         return attributes.filter(value__in=selected_values)

#     def get_numeric_ranges_filtered_attributes(self, ranges):
#         if self.filter_type != 'NUMERIC_RANGES':
#             raise exceptions.ProductFilterFilterException('Wrong filter function')
#         attributes = self.get_related_attributes()
#         query = Q()
#         for min_value, max_value in ranges:
#             query = query | (Q(value_float__gte=min_value) & Q(value_float__lte=max_value))
#         return attributes.filter(query)
