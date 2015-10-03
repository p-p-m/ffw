# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from .exceptions import CartException
from constance import config
from products.models import ProductConfiguration


# TODO: rewrite messages
class Order(TimeStampedModel):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    name = models.CharField(_('Name'), max_length=255)
    email = models.EmailField(_('E-mail'), max_length=125, blank=True)
    phone = models.CharField(_('Phone'), max_length=125)
    contacts = models.TextField(_('Additional contacts'), blank=True)
    total = models.DecimalField(_('Total'), decimal_places=2, max_digits=9, default=0)
    count = models.IntegerField(_('Quantity'), default=0)
    is_resolved = models.BooleanField(_('Is order resolved'), default=False)

    def __str__(self):
        return 'order #{}'.format(self.id)

    def _get_user_message(self):
        return (
            "Успешно оформлен заказ на сайте ffw. Номер заказа {}. Cумма заказа {} грн.\n\n"
            "Детали заказа:\n"
            "{}\n\n"
            "Наши контакты:\n"
            "(044) 510-91-03\n"
            "(067) 417-00-21\n"
            "(050) 520-00-21\n"
            "Email: info@waterproff.ua\n"
        ).format(
            self.pk,
            self.total,
            '\n'.join([p.to_representaion() for p in self.products.all()]),
        )

    def _get_admin_message(self):
        return (
            "Получен новый заказ на сайте ffw. На сумму {} грн.\n\n"
            "Детали заказа:\n"
            "{}\n\n"
            "Контакты заказчика:\n"
            "Имя: {}\n"
            "Email: {}\n"
            "Телефон: {}\n"
            "Другие контакты: {}\n"
        ).format(
            self.total,
            '\n'.join([p.to_representaion() for p in self.products.all()]),
            self.name,
            self.email,
            self.phone,
            self.contacts
        )

    # TODO: Make this call async.
    def send_customer_email(self):
        if self.email:
            send_mail(
                'Успешно оформлен заказ на сайте ffw. Номер заказа: {}'.format(self.id),
                self._get_user_message(),
                settings.EMAIL_HOST_USER,
                [self.email],
            )
        # if self.email:
        #     thr = threading.Thread(
        #         target=send_mail,
        #         args=(
        #             'Успешно оформлен заказ на сайте ffw. Номер заказа: {}'.format(self.id),
        #             self._get_user_message(),
        #             settings.EMAIL_HOST_USER,
        #             [self.email],
        #         ),
        #         kwargs={
        #             'fail_silently': True
        #         },
        #     )
        #     thr.start()
        # return thr

    def send_admin_email(self):
        send_mail(
            'Новый заказ на сайте ffw. Номер заказа: {}'.format(self.id),
            self._get_admin_message(),
            settings.EMAIL_HOST_USER,
            [email.strip() for email in config.ADMIN_EMAILS.split(',')],
        )
        # thr = threading.Thread(
        #     target=send_mail,
        #     args=(

        #     ),
        #     kwargs={
        #         'fail_silently': True
        #     },
        # )
        # thr.start()
        # return thr


class OrderedProduct(models.Model):
    class Meta:
        verbose_name = _('Ordered products')
        verbose_name_plural = _('Ordered products')

    order = models.ForeignKey(Order, verbose_name='Order', related_name='products')
    # XXX: This FK provides circular dependency in applications cart and products. We need to use abstract product
    # from cart settings. Also FK should be nullable
    product = models.ForeignKey(ProductConfiguration, verbose_name='Product', related_name='ordered_product')
    name = models.CharField(_('Name'), max_length=127)
    code = models.CharField(_('Code'), max_length=127)
    price = models.DecimalField(_('Price'), decimal_places=2, max_digits=7)
    quant = models.IntegerField(_('Quantity'), default=0)
    total = models.DecimalField(_('Total'), decimal_places=2, max_digits=9)

    def __str__(self):
        return u'Product with id: {}'.format(self.product.id)

    def to_representaion(self):
        return ' - {} ({}): количество: {}, сумма {}, (цена за единицу продукта {});'.format(
            self.name, self.code, self.quant, self.total, self.price)


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
        return str(self.product.pk)


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
                'code': product.code,
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
        product = CartProduct(product_pk)

        if product.pk_str in self.cart['products'].keys():
            self.cart['products'][product.pk_str]['quant'] += quant
            self.cart['products'][product.pk_str]['sum_'] = float(
                self.cart['products'][product.pk_str]['quant'] * product.price)
        else:
            self.set(product_pk, quant)

        self._calculate()
