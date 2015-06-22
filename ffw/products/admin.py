from django import forms
from django.contrib import admin

from . import models
# XXX: this is fragile import that creates circular dependency between applications.
#      However it is hard to implement it in other way in django admin :(
#      This will be corrected then custom admin panel will be implemented
from assembly import models as assembly_models


class BaseFilterInline(admin.TabularInline):
    extra = 1

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(BaseFilterInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'characteristic':
            if request._obj_ is not None:
                field.queryset = request._obj_.characteristics.all()
            else:
                field.queryset = field.queryset.none()

        return field


class NumericAttributeFilterInline(BaseFilterInline):
    model = assembly_models.NumericAttributeFilter
    fields = ('characteristic', 'max_value', 'min_value', 'priority')


class ChoicesAttributeFilterInline(BaseFilterInline):
    model = assembly_models.ChoicesAttributeFilter
    fields = ('characteristic', 'choices', 'priority')


class IntervalsAttributeFilterInline(BaseFilterInline):
    model = assembly_models.IntervalsAttributeFilter
    fields = ('characteristic', 'intervals', 'priority')


class CharacteristicAdmin(admin.ModelAdmin):
    model = models.Characteristic
    list_display = ('name', 'default_value', 'units',)
    search_fields = ('name', 'units')


class BaseCategoryAdmin(admin.ModelAdmin):
    inlines = (
        NumericAttributeFilterInline,
        ChoicesAttributeFilterInline,
        IntervalsAttributeFilterInline,
    )

    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ('characteristics',)

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(BaseCategoryAdmin, self).get_form(request, obj, **kwargs)


class SectionAdmin(BaseCategoryAdmin):
    model = models.Section
    list_display = ('name',)


class CategoryAdmin(BaseCategoryAdmin):
    model = models.Category
    list_display = ('name', 'section')


class SubcategoryAdmin(BaseCategoryAdmin):
    model = models.Subcategory
    list_display = ('name', 'category')


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
    readonly_fields = ('preview', )

    def preview(self, obj):
        if obj is None:
            return
        return '<strong><a href="' + obj.get_url() + '" target="_blank"> Project on site </a></strong>'


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


admin.site.register(models.Section, SectionAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Subcategory, SubcategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductFilter, ProductFilterAdmin)
admin.site.register(models.Characteristic, CharacteristicAdmin)
