# coding: utf-8
from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _

from . import handlers


class CartConfig(AppConfig):
    name = 'cart'
    verbose_name = _('Cart')

    def ready(self):
        Order = self.get_model('Order')

        signals.post_save.connect(
            handlers.send_emails_on_order_creation,
            sender=Order,
            dispatch_uid='cart.handlers.send_emails_on_order_creation',
        )
