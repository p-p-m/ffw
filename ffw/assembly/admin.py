"""
This file is showing admin model for developers and water filters only.
All custom admin views have to be located in application 'admin'.
"""
import re

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.utils.functional import curry

from assembly import models as assembly_models
from products import models as products_models


class BaseFilterInline(admin.TabularInline):
    extra = 1

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(BaseFilterInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'characteristic':
            if request._obj_ is not None:
                field.queryset = request._obj_.characteristics.filter(is_default=False).all()
            else:
                field.queryset = field.queryset.none()

        return field

    def get_max_num(self, request, obj=None, **kwargs):
        if request._obj_ is None:
            return 0
        return super(BaseFilterInline, self).get_max_num(request, obj, **kwargs)


class NumericAttributeFilterInline(BaseFilterInline):
    model = assembly_models.NumericAttributeFilter
    fields = ('name', 'characteristic', 'max_value', 'min_value', 'is_auto_update', 'priority')


class ChoicesAttributeFilterInline(BaseFilterInline):
    model = assembly_models.ChoicesAttributeFilter
    fields = ('name', 'characteristic', 'choices', 'is_auto_update', 'priority')


class IntervalsAttributeFilterInline(BaseFilterInline):
    model = assembly_models.IntervalsAttributeFilter
    fields = ('name', 'characteristic', 'intervals', 'priority')


class CharacteristicAdmin(admin.ModelAdmin):
    model = products_models.Characteristic
    list_display = ('name', 'default_value', 'units',)
    search_fields = ('name', 'units')


FILTER_INLINES = (
    NumericAttributeFilterInline,
    ChoicesAttributeFilterInline,
    IntervalsAttributeFilterInline,
)


class BaseCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ('characteristics',)

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(BaseCategoryAdmin, self).get_form(request, obj, **kwargs)


class SectionCharacteristicInline(admin.TabularInline):
    model = products_models.SectionCharacteristic
    fields = ('characteristic',)
    extra = 1


class SectionAdmin(BaseCategoryAdmin):
    inlines = (SectionCharacteristicInline, ) + FILTER_INLINES
    model = products_models.Section
    list_display = ('name',)


class CategoryCharacteristicInline(admin.TabularInline):
    model = products_models.CategoryCharacteristic
    fields = ('characteristic',)
    extra = 1


class CategoryAdmin(BaseCategoryAdmin):
    model = (CategoryCharacteristicInline, ) + FILTER_INLINES
    list_display = ('name', 'section')


class SubcategoryCharacteristicInline(admin.TabularInline):
    model = products_models.SubcategoryCharacteristic
    fields = ('characteristic',)
    extra = 1

    def get_max_num(self, request, obj=None, **kwargs):
        return products_models.Characteristic.objects.count()


class SubcategoryAdmin(BaseCategoryAdmin):
    inlines = (SubcategoryCharacteristicInline, ) + FILTER_INLINES
    model = products_models.Subcategory
    list_display = ('name', 'category')


class ProductConfigurationForm(forms.ModelForm):
    attributes = forms.CharField(label='Attributes', widget=widgets.Textarea)

    class Meta:
        model = products_models.ProductConfiguration
        fields = ['code', 'price_uah', 'price_usd', 'price_eur', 'is_active']

    def __init__(self, *args, **kwargs):
        super(ProductConfigurationForm, self).__init__(*args, **kwargs)
        if self.instance.id is not None:
            self.fields['attributes'].initial = '\n'.join('{}: {} ({})'.format(
                a.name, a.value, a.units) for a in self.instance.attributes.all())

    def clean_attributes(self):
        attributes = self.cleaned_data['attributes']
        if len(attributes.split('\n')) < len(self.fields['attributes'].initial.split('\n')):
            raise ValidationError('Not enough attributes provided')
        result_attribures = []
        for attr in attributes.split('\n'):
            parsed_attr = re.findall('(.+):(.*)\((.*)\)', attr)
            if parsed_attr:
                name, value, units = [el.strip() for el in parsed_attr[0]]
                result_attribures.append({'name': name, 'value': value, 'units': units})
            else:
                raise ValidationError(
                    'Attribute "%(attr)s" is not recognized it has to follow patter: <name>: <value> (<units>)',
                    params={'attr': attr},)
        return result_attribures

    def save(self, *args, **kwargs):
        configuration = super(ProductConfigurationForm, self).save(*args, **kwargs)
        for attribute in self.cleaned_data['attributes']:
            if not configuration.attributes.filter(**attribute).exists():
                configuration.attributes.update_or_create(name=attribute.pop('name'), defaults=attribute)


class ProductConfigurationInline(admin.TabularInline):
    model = products_models.ProductConfiguration
    extra = 0
    form = ProductConfigurationForm
    fieldsets = (
        (None, {
            'fields': ('code', 'attributes', 'is_active', 'price_uah', 'price_usd', 'price_eur',),
        }),
    )

    def get_max_num(self, request, obj=None, **kwargs):
        if obj is None:
            return 0
        return super(ProductConfigurationInline, self).get_max_num(request, obj, **kwargs)

    def get_extra(self, request, obj=None, **kwargs):
        if obj is None:
            return 0
        return 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(ProductConfigurationInline, self).get_formset(request, obj, **kwargs)
        if request._obj_ is not None:
            characteristics = request._obj_.get_characteristics()
            s = '\n'.join('{}: {} ({})'.format(c.name, c.default_value, c.units) for c in characteristics)
            initial = [{
                'attributes': s,
            }] * 4
            formset.__init__ = curry(formset.__init__, initial=initial)

            # Brutal hook to add initial values to new configurations
            def formset_empty_form(self):
                form = self.form(
                    auto_id=self.auto_id,
                    prefix=self.add_prefix('__prefix__'),
                    empty_permitted=True,
                    initial={'attributes': s}
                )
                self.add_fields(form, None)
                return form
            formset.empty_form = property(formset_empty_form)

        return formset


class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductConfigurationInline, )
    model = products_models.Product
    list_display = ('name', 'is_active', 'modified', 'created')
    ordering = ('modified', 'name')
    search_fields = ('name', )
    list_filter = ('is_active',)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('preview', )

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(ProductAdmin, self).get_form(request, obj, **kwargs)

    def preview(self, obj):
        if obj is None:
            return
        return 'qqw'
        return '<strong><a href="' + obj.get_url() + '" target="_blank"> Project on site </a></strong>'


admin.site.register(products_models.Section, SectionAdmin)
admin.site.register(products_models.Category, CategoryAdmin)
admin.site.register(products_models.Subcategory, SubcategoryAdmin)
admin.site.register(products_models.Product, ProductAdmin)
admin.site.register(products_models.Characteristic, CharacteristicAdmin)
