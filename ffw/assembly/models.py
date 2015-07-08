from django.db import models

from filters.models import NumericFilterMixin, ChoicesFilterMixin, IntervalsFilterMixin
from products import models as products_models

from .managers import ProductFilterManager


class BaseFilter(models.Model):
    class Meta:
        abstract = True

    objects = ProductFilterManager()

    section = models.ForeignKey(products_models.Section, null=True)
    category = models.ForeignKey(products_models.Category, null=True)
    subcategory = models.ForeignKey(products_models.Subcategory, null=True)
    characteristic = models.ForeignKey(products_models.Characteristic)

    def get_attribute_query(self):
        return models.Q(attributes__name=self.characteristic.name)


class NumericAttributeFilter(NumericFilterMixin, BaseFilter):

    def _get_min_and_max(self, request):
        selected_max_value = request.GET.get('{}-max'.format(self.get_item_prefix()), self.max_value)
        selected_min_value = request.GET.get('{}-min'.format(self.get_item_prefix()), self.min_value)
        return selected_min_value, selected_max_value

    def filter(self, queryset, request):
        attribute_query = self.get_attribute_query()
        selected_min_value, selected_max_value = self._get_min_and_max(request)
        filter_query = self.get_filter_query('attributes__value_float', selected_min_value, selected_max_value)
        return queryset.filter(attribute_query, filter_query)

    def update(self):
        return super(NumericAttributeFilter, self).base_update(field='value_float')


class ChoicesAttributeFilter(ChoicesFilterMixin, BaseFilter):

    def _get_choices(self, request):
        choices = []
        for index, choice in enumerate(self.get_formatted_choices()):
            if '{}-{}'.format(self.get_item_prefix(), index) in request.GET:
                choices.append(choice)
        return choices

    def filter(self, queryset, request):
        attribute_query = self.get_attribute_query()
        choices = self._get_choices(request)
        filter_query = self.get_filter_query('attributes__value', choices)
        return queryset.filter(attribute_query, filter_query)

    def update(self):
        return super(ChoicesAttributeFilter, self).base_update(field='value')


class IntervalsAttributeFilter(IntervalsFilterMixin, BaseFilter):

    def _get_intervals(self, request):
        intervals = []
        for index, choice in enumerate(self.get_formatted_intervals()):
            if '{}-{}'.format(self.get_item_prefix(), index) in request.GET:
                intervals.append(choice)
        return intervals

    def filter(self, queryset, request):
        intervals = self._get_intervals(request)
        if not intervals:
            return queryset
        attribute_query = self.get_attribute_query()
        filter_query = self.get_filter_query('attributes__value', intervals)
        return queryset.filter(attribute_query, filter_query)
