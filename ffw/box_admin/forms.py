from django import forms

from products import models as products_models


class ProductForm(forms.ModelForm):
    class Meta:
        model = products_models.Product
        fields = ['name', 'subcategory', 'short_description', 'description', 'is_active']


class ProductConfigurationForm(forms.ModelForm):
    class Meta:
        model = products_models.ProductConfiguration
        fields = ['code', 'is_active', 'product']
