from django import forms
from django.db.models import Count, Min, Max
from django.utils.translation import ugettext_lazy as _

import models


class SortForm(forms.Form):
    SORT_CHOICES = (
        ('PA', _('Price, from small to big')),
        ('PD', _('Price, from big to small')),
        ('RD', _('Rating, from big to small')),
    )

    sort_by = forms.ChoiceField(choices=SORT_CHOICES)

    def sort(self, queryset):
        sort_by = self.cleaned_data['sort_by']
        if sort_by == 'PA':
            queryset = queryset.annotate(null_price=Count('price_uah')).order_by('-null_price', 'price_uah')
        elif sort_by == 'PD':
            queryset = queryset.order_by('-price_uah')
        elif sort_by == 'RD':
            queryset = queryset.order_by('-rating')
        return queryset


class FilterForm(forms.Form):

    def __init__(self, category=None, subcategory=None, **kwargs):
        super(FilterForm, self).__init__(**kwargs)
        self.filters = self._get_filters(category, subcategory)
        for filt in self.filters:
            self.fields.update(self._create_filter_fields(filt))
        prices = self._get_base_queryset(category, subcategory).aggregate(Min('price_uah'), Max('price_uah'))

        self.fields['price_min'] = forms.FloatField(
            label='Min price', required=False,
            min_value=int(prices['price_uah__min']), max_value=int(prices['price_uah__max']) + 1)
        self.fields['price_max'] = forms.FloatField(
            label='Min price', required=False,
            min_value=int(prices['price_uah__min']), max_value=int(prices['price_uah__max']) + 1)

    def _get_filters(self, category=None, subcategory=None):
        filters = []
        if category is not None:
            filters += list(models.ProductFilter.objects.filter(category=category))
        if subcategory is not None:
            filters += list(models.ProductFilter.objects.filter(subcategory=subcategory))
        return filters

    def _get_base_queryset(self, category=None, subcategory=None):
        queryset = models.Product.objects.all()
        if category is not None:
            queryset = queryset.filter(subcategory__category=category)
        if subcategory is not None:
            queryset = queryset.filter(subcategory=subcategory)
        return queryset

    def _create_filter_fields(self, filt):
        if filt.filter_type == 'NUMERIC':
            attrs = {'min-value': filt.values['min'], 'max-value': filt.values['max']}
            fields = {
                'numeric_%s_min' % filt.pk: forms.FloatField(
                    label='Min', required=False, min_value=filt.values['min'], max_value=filt.values['max']),
                'numeric_%s_max' % filt.pk: forms.FloatField(
                    label='Max', required=False, min_value=filt.values['min'], max_value=filt.values['max']),
            }
            for field in fields.itervalues():
                field.widget.attrs = attrs
            return fields
        elif filt.filter_type == 'CHOICES':
            fields = {}
            for index, choice in enumerate(filt.values['choices']):
                fields['choices_%s_%s' % (filt.pk, index)] = forms.BooleanField(label=choice, required=False)
            return fields
        elif filt.filter_type == 'NUMERIC_RANGES':
            fields = {}
            for index, numeric_range in enumerate(filt.values['ranges']):
                label = '%s - %s' % (numeric_range[0], numeric_range[1])
                fields['numeric_ranges_%s_%s' % (filt.pk, index)] = forms.BooleanField(label=label, required=False)
            return fields

    def _get_filter_fields(self, filt):
        field_name_prefix = '%s_%s' % (filt.filter_type.lower(), filt.pk)
        return {name: field for name, field in self.fields.iteritems() if name.startswith(field_name_prefix)}

    def filter_products(self, products_queryset):
        cd = self.cleaned_data
        for filt in self.filters:
            attributes_ids = None
            fields = self._get_filter_fields(filt)

            if filt.filter_type == 'CHOICES':
                selected_values = [field.label for name, field in fields.iteritems() if name in cd and cd[name]]
                if selected_values:
                    attributes_ids = filt.get_choices_filtered_attributes(
                        selected_values).values_list('id', flat=True)

            elif filt.filter_type == 'NUMERIC_RANGES':
                fields_labels = [field.label for name, field in fields.iteritems() if name in cd and cd[name]]
                ranges = [[float(n.strip()) for n in label.split('-')] for label in fields_labels]
                if ranges:
                    attributes_ids = filt.get_numeric_ranges_filtered_attributes(ranges).values_list('id', flat=True)

            elif filt.filter_type == 'NUMERIC':
                max_min = {name[-3:]: cd[name] for name in fields if name in cd and cd[name] is not None}
                if max_min:
                    attributes_ids = filt.get_numeric_filtered_attributes(max_min.get('min'), max_min.get('max'))

            if attributes_ids is not None:
                products_queryset = products_queryset.filter(attributes__in=attributes_ids)

        price_min = cd.get('price_min')
        price_max = cd.get('price_max')
        if price_min is not None:
            products_queryset = products_queryset.filter(price_uah__gte=price_min)
        if price_max is not None:
            products_queryset = products_queryset.filter(price_uah__lte=price_max)

        return products_queryset

    @property
    def price_fields(self):
        return {f.name: f for f in self if f.name.startswith('price')}

    @property
    def fields_groups(self):
        """
        Returns form fields grouped by filters
        """
        for filt in self.filters:
            field_name_prefix = '%s_%s' % (filt.filter_type.lower(), filt.pk)
            yield {
                'id': filt.id,
                'name': filt.name,
                'type': filt.filter_type.lower(),
                'fields': [f for f in self if f.name.startswith(field_name_prefix)],
            }
