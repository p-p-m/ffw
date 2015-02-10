from django import forms
from django.contrib import admin

import models


class CategoryAdmin(admin.ModelAdmin):
    model = models.Category
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class SubcategoryAdmin(admin.ModelAdmin):
    model = models.Subcategory
    list_display = ('name', 'category')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class ProductAttributeInline(admin.TabularInline):
    model = models.ProductAttribute
    extra = 2


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = (
        ProductAttributeInline,
        ProductImageInline,
    )
    model = models.Product
    list_display = ('name', 'code', 'price_uah', 'price_usd', 'price_eur', 'is_active', 'modified', 'created')
    ordering = ('modified', 'name')
    search_fields = ('name', 'code', 'price_uah', 'price_usd', 'price_eur')
    list_filter = ('is_active',)
    prepopulated_fields = {"slug": ("name",)}


class ProductFilterAdmin(admin.ModelAdmin):
    model = models.ProductFilter
    list_display = ('name', 'filter_type', 'attribute_name', 'category', 'subcategory')
    search_fields = ('name', 'attribute_name', 'category__name', 'subcategory__name')
    list_filter = ('filter_type',)
    prepopulated_fields = {"name": ("attribute_name",)}

    def formfield_for_dbfield(self, db_field, **kwargs):
        if str(db_field) == 'products.ProductFilter.attribute_name':
            attributes = ((name, name) for name in set(models.ProductAttribute.objects.values_list('name', flat=True)))
            return forms.ChoiceField(choices=attributes)
        return super(ProductFilterAdmin, self).formfield_for_dbfield(db_field, **kwargs)


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Subcategory, SubcategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductFilter, ProductFilterAdmin)
