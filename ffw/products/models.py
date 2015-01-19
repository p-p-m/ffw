from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=127)


class Subcategory(models.Model):
    name = models.CharField(max_length=127)
    category = models.ForeignKey(Category)
