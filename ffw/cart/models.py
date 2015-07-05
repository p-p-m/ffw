# coding: utf-8
from __future__ import unicode_literals

from django.db import models


class TestProduct(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=127, unique=True)
    price_uah = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
