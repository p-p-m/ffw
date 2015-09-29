# coding: utf-8
from __future__ import unicode_literals

import collections
import logging

from constance import config
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.encoding import python_2_unicode_compatible
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from model_utils import FieldTracker
from model_utils.models import TimeStampedModel
from unidecode import unidecode

from core.models import ImageFieldWaterMark

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
    rating = models.FloatField(
        _('Rating'), default=4.0,
        help_text=_('Characteristic with higher ratings will be displayed first'))

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
    image = ImageFieldWaterMark(upload_to='categories/', verbose_name=_('Image'), blank=True)
    image_small_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=150, height=150, upscale=True, mat_color='white')],
        format='JPEG',
        options={'quality': 100})
    image_big_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=1000, height=1000, upscale=True, mat_color='white')],
        format='JPEG',
        options={'quality': 100})

    def __str__(self):
        return '{}-{}'.format(self.section, self.name)

    def get_url(self):
        return reverse('products', args=(self.section.slug, self.slug))

    def get_subcategories(self):
        return self.subcategories.all().distinct()


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
    image = ImageFieldWaterMark(upload_to='subcategories/', verbose_name=_('Image'), blank=True)
    image_small_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=120, height=120, upscale=True, mat_color='white')],
        format='JPEG',
        options={'quality': 100})
    image_big_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=1000, height=1000, upscale=True, mat_color='white')],
        format='JPEG',
        options={'quality': 100})

    is_on_main_page = models.BooleanField(_('Is on main page'), default=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.category.section.name, self.category.name, self.name)

    def get_url(self):
        return reverse('products', args=(self.category.section.slug, self.category.slug, self.slug))

    def get_all_related_characteristics(self):
        query = (
            models.Q(subcategories=self) |
            models.Q(categories=self.category) |
            models.Q(sections=self.category.section)
        )
        return Characteristic.objects.filter(query).distinct()


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
    price_min = models.DecimalField(_('Max price in UAH'), null=True, max_digits=10, decimal_places=2)
    price_max = models.DecimalField(_('Min price in UAH'), null=True, max_digits=10, decimal_places=2)

    materials = models.ForeignKey(Subcategory, verbose_name=_('Consumables and accessories'), null=True, blank=True)

    tracker = FieldTracker()

    def __str__(self):
        return '{}'.format(self.name)

    def clean(self):
        # if subcategory changed
        if Product.objects.filter(id=self.id).exclude(subcategory=self.subcategory).exists():
            characteristics_names = set(self.subcategory.get_all_related_characteristics().values_list(
                'name', flat=True))
            for configuration in self.configurations.all():
                attributes_names = set(configuration.attributes.values_list('name', flat=True))
                missing_attributes = characteristics_names - attributes_names
                if missing_attributes:
                    raise ValidationError(
                        ugettext('Product configuration %(configuration_code)s does not have attributes with '
                                 'names: %(missing_attributes)s. They are required for new subcategory.') % {
                            'configuration_code': configuration.code,
                            'missing_attributes': ', '.join(missing_attributes),
                            }
                        )

    def get_url(self):
        return reverse('product', args=(self.slug, ))

    def get_images(self):
        return self.images.all()

    def get_first_image(self):
        image = self.images.filter(is_main=True).first()
        if image is None:
            image = self.images.first()
        return image

    def get_characteristics(self):
        query = (
            models.Q(categories=self.subcategory.category) |
            models.Q(subcategories=self.subcategory) |
            models.Q(sections=self.subcategory.category.section)
        )
        return Characteristic.objects.filter(query).distinct()

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        return super(Product, self).save(*args, **kwargs)

    def get_display_price_uah(self):
        if self.price_min is None:
            return
        if self.price_min != self.price_max:
            return '{}-{}'.format(self.price_min, self.price_max)
        else:
            return self.price_min

    def get_attributes(self):
        """
        Return all attributes if product has one configuration, else return common attributes for configurations
        """
        attributes = ProductAttribute.objects.filter(product_configuration__product=self).order_by(
            '-characteristic__rating')
        if self.configurations.count() > 1:
            configurations_attribures_names = [set(c.attributes.all().values_list('name', 'value'))
                                               for c in self.configurations.all()]
            equal_attribures = reduce(lambda x, y: x & y, configurations_attribures_names)
            return attributes.filter(
                name__in=[name for name, _ in equal_attribures], product_configuration=self.configurations.all()[0])
        else:
            return attributes

    def recalculate_prices(self):
        self.price_max = self.configurations.aggregate(models.Max('price_uah'))['price_uah__max']
        self.price_min = self.configurations.aggregate(models.Min('price_uah'))['price_uah__min']

    def get_materials(self):
        if self.materials:
            return self.materials.products.all()[:8]

    def get_products_with_same_name(self):
        return Product.objects.filter(name=self.name)[:8]

    # XXX: This method is too complex we need to do it in other way
    def get_similar_products(self):
        attributes = ProductAttribute.objects.filter(product_configuration__product=self)
        similar_products_groups = [list(Product.objects.filter(configurations__attributes__name=attribute.name,
                                                               configurations__attributes__value=attribute.value,
                                                               subcategory__category=self.subcategory.category))
                                   for attribute in attributes]
        similar_products = sum(similar_products_groups, [])
        return collections.Counter(similar_products).keys()[:4]

    def get_approved_comments(self):
        return self.comments.filter(is_approved=True)


@python_2_unicode_compatible
class ProductConfiguration(models.Model):
    class Meta:
        verbose_name = _('Product configuration')
        verbose_name_plural = _('Product configurations')

    product = models.ForeignKey(Product, verbose_name=_('Product'), related_name='configurations')
    code = models.CharField(_('Code'), max_length=127, unique=True)
    is_active = models.BooleanField(_('Is active'), default=True)
    price_uah = models.DecimalField(_('Price in UAH'), null=True, max_digits=10, decimal_places=2)
    price_eur = models.DecimalField(_('Price in EUR'), null=True, max_digits=10, decimal_places=2)
    price_usd = models.DecimalField(_('Price in USD'), null=True, max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}-{}'.format(self.product, self.code)

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
                attr, created = self.attributes.get_or_create(name=key)
                attr.value = value
                attr.save()

        return Attrs()

    def init_prices(self):
        value = None
        if self.price_uah:
            value = float(self.price_uah)
        elif self.price_usd:
            value = float(self.price_usd) * config.USD_RATE
        elif self.price_eur:
            value = float(self.price_eur) * config.EUR_RATE

        if value is not None:
            if not self.price_uah:
                self.price_uah = value
            if not self.price_usd:
                self.price_usd = value / config.USD_RATE
            if not self.price_eur:
                self.price_eur = value / config.EUR_RATE

    def get_unique_attributes(self):
        common_attributes = self.product.get_attributes()
        return self.attributes.exclude(name__in=common_attributes.values_list('name', flat=True)).order_by(
            '-characteristic__rating')

    def get_formatted_unique_attributes(self):
        unique_attributes = self.get_unique_attributes()
        return ', '.join(['{}: {}'.format(a.name, a.pretty_value) for a in unique_attributes])

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

    def connect_with_characteristic(self, subcategory=None, save=False):
        """ Find characteristic that related to this attribute and connect to it """
        subcategory = self.product_configuration.product.subcategory if subcategory is None else subcategory
        try:
            c = subcategory.get_all_related_characteristics().get(name=self.name)
            self.characteristic = c
            self.units = c.units
            if save:
                self.save()
        except Characteristic.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        self._init_values()
        return super(ProductAttribute, self).save(*args, **kwargs)

    @property
    def pretty_value(self):
        if self.units:
            return '{} ({})'.format(self.value, self.units)
        else:
            return self.value


class ProductImage(models.Model):
    class Meta:
        verbose_name = _('Product image')
        verbose_name_plural = _('Product images')

    product = models.ForeignKey(Product, related_name='images')
    image = ImageFieldWaterMark(upload_to='products/', verbose_name=_('Image'))
    image_small_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=200, height=200, upscale=True, mat_color='white')],
        format='JPEG',
        options={'quality': 100})
    image_big_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=1000, height=1000, upscale=True, mat_color='white')],
        format='JPEG',
        options={'quality': 100})
    description = models.CharField(_('Image description'), max_length=127, blank=True)
    is_main = models.BooleanField(
        default=True,
        help_text=_('If image is main - it will be displayed on product list page'))


class Comment(TimeStampedModel):
    class Meta:
        verbose_name = _('Product comment')
        verbose_name_plural = _('Product comments')

    product = models.ForeignKey(Product, related_name='comments')
    positive_sides = models.TextField(_('Positive sides'), blank=True)
    negative_sides = models.TextField(_('Negative sides'), blank=True)
    is_approved = models.BooleanField(
        _('Is approved by stuff'),
        default=False,
        help_text=_('Only approved comments is visible for users')
    )
