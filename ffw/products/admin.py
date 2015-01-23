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


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Subcategory, SubcategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
