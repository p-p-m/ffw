from django.db import models

from filters.models import NumericFilterMixin, ChoicesFilterMixin, IntervalsFilterMixin
from products.models import Characteristic, Section, Category, Subcategory


class BaseFilter(models.Model):
    class Meta:
        abstract = True

    section = models.ForeignKey(Section, null=True)
    category = models.ForeignKey(Category, null=True)
    subcategory = models.ForeignKey(Subcategory, null=True)


class BaseAttributeFilter(BaseFilter):
    characteristic = models.ForeignKey(Characteristic)

    class Meta:
        abstract = True

    def get_attribute_query(self):
        return models.Q(attributes__name=self.characteristic.name)


class NumericAttributeFilter(NumericFilterMixin, BaseAttributeFilter):

    def _get_min_and_max(self, request):
        selected_max_value = request.GET.get('{}-max'.format(self.get_item_prefix()), self.max_value)
        selected_min_value = request.GET.get('{}-min'.format(self.get_item_prefix()), self.min_value)
        return selected_min_value, selected_max_value

    def filter(self, queryset, request):
        attribute_query = self.get_attribute_query()
        selected_min_value, selected_max_value = self._get_min_and_max(request)
        filter_query = self.get_filter_query('attributes__value_float', selected_min_value, selected_max_value)
        return queryset.filter(attribute_query, filter_query)


class ChoicesAttributeFilter(ChoicesFilterMixin, BaseAttributeFilter):

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


class IntervalsAttributeFilter(IntervalsFilterMixin, BaseAttributeFilter):

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


# Do we need this fields?
# class BaseFieldFilter(BaseFilter):
#     field_name = models.CharField(max_length=50)

#     class Meta:
#         abstract = True


# class NumericFieldFilter(NumericFilterMixin, BaseFieldFilter):

#     def filter(self, queryset, selected_max_value, selected_min_value):
#         filter_query = self.get_filter_query(self.field_name, selected_min_value, selected_max_value)
#         return queryset.filter(filter_query)


# class ChoicesFieldFilter(ChoicesFilterMixin, BaseFieldFilter):

#     def filter(self, queryset, choices):
#         filter_query = self.get_filter_query(self.field_name, choices)
#         return queryset.filter(filter_query)


# class IntervalsFieldFilter(IntervalsFilterMixin, BaseFieldFilter):

#     def filter(self, queryset, intervals):
#         filter_query = self.get_filter_query(self.field_name, intervals)
#         return queryset.filter(filter_query)
