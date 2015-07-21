from django.db import models

from filters.models import NumericFilterMixin, ChoicesFilterMixin, IntervalsFilterMixin
from products import models as products_models

from .managers import ProductFilterManager


def get_category_filters(category):
    return (
        list(NumericAttributeFilter.objects.filter(category=category)) +
        list(ChoicesAttributeFilter.objects.filter(category=category)) +
        list(IntervalsAttributeFilter.objects.filter(category=category)) +
        list(NumericPriceFilter.objects.filter(category=category))
    )


def get_subcategory_filters(subcategory):
    return (
        list(NumericAttributeFilter.objects.filter(subcategory=subcategory)) +
        list(ChoicesAttributeFilter.objects.filter(subcategory=subcategory)) +
        list(IntervalsAttributeFilter.objects.filter(subcategory=subcategory)) +
        list(NumericPriceFilter.objects.filter(subcategory=subcategory))
    )


def get_section_filters(section):
    return (
        list(NumericAttributeFilter.objects.filter(section=section)) +
        list(ChoicesAttributeFilter.objects.filter(section=section)) +
        list(IntervalsAttributeFilter.objects.filter(section=section)) +
        list(NumericPriceFilter.objects.filter(section=section))
    )


class BaseFilter(models.Model):
    class Meta:
        abstract = True

    objects = ProductFilterManager()

    section = models.ForeignKey(products_models.Section, null=True)
    category = models.ForeignKey(products_models.Category, null=True)
    subcategory = models.ForeignKey(products_models.Subcategory, null=True)

    def get_related_products(self):
        query = (
            models.Q(subcategory__category__section=self.section) |
            models.Q(subcategory__category=self.category) |
            models.Q(subcategory=self.subcategory)
        )
        return products_models.Product.objects.filter(query)


class NumericPriceFilter(NumericFilterMixin, BaseFilter):

    def _get_min_and_max(self, request):
        selected_max_value = request.GET.get('{}-max'.format(self.get_item_prefix()), self.max_value)
        selected_min_value = request.GET.get('{}-min'.format(self.get_item_prefix()), self.min_value)
        return selected_min_value, selected_max_value

    def filter(self, queryset, request):
        selected_min_value, selected_max_value = self._get_min_and_max(request)
        filter_query = self.get_filter_query('price_uah', selected_min_value, selected_max_value)
        return queryset.filter(filter_query)

    def update(self):
        return super(NumericPriceFilter, self).base_update(field='price_uah')

    def get_queryset(self):
        products = self.get_related_products()
        return products_models.ProductConfiguration.objects.filter(product__in=products)


class BaseCharacteristicFilter(BaseFilter):
    class Meta:
        abstract = True

    characteristic = models.ForeignKey(products_models.Characteristic)

    def get_attribute_query(self):
        return models.Q(attributes__name=self.characteristic.name)


class NumericAttributeFilter(NumericFilterMixin, BaseCharacteristicFilter):

    def _get_min_and_max(self, request):
        selected_max_value = request.GET.get('{}-max'.format(self.get_item_prefix()), self.max_value)
        selected_min_value = request.GET.get('{}-min'.format(self.get_item_prefix()), self.min_value)
        return selected_min_value, selected_max_value

    def filter(self, queryset, request):
        attribute_query = self.get_attribute_query()
        selected_min_value, selected_max_value = self._get_min_and_max(request)
        filter_query = self.get_filter_query('attributes__value_float', selected_min_value, selected_max_value)
        print 'FITLER QUERY', filter_query
        return queryset.filter(attribute_query, filter_query)

    def update(self):
        return super(NumericAttributeFilter, self).base_update(field='value_float')

    def get_queryset(self):
        products = self.get_related_products()
        return products_models.ProductAttribute.objects.filter(product_configuration__product__in=products)


class ChoicesAttributeFilter(ChoicesFilterMixin, BaseCharacteristicFilter):

    def _get_choices(self, request):
        choices = []
        for index, choice in enumerate(self.get_formatted_choices()):
            if '{}-{}'.format(self.get_item_prefix(), index) in request.GET:
                choices.append(choice)
        return choices

    def filter(self, queryset, request):
        attribute_query = self.get_attribute_query()
        choices = self._get_choices(request)
        if choices:
            filter_query = self.get_filter_query('attributes__value', choices)
            queryset = queryset.filter(attribute_query, filter_query)
        return queryset

    def update(self):
        return super(ChoicesAttributeFilter, self).base_update(field='value')

    def get_queryset(self):
        products = self.get_related_products()
        return products_models.ProductAttribute.objects.filter(product_configuration__product__in=products)


class IntervalsAttributeFilter(IntervalsFilterMixin, BaseCharacteristicFilter):

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

    def get_queryset(self):
        products = self.get_related_products()
        return products_models.ProductAttribute.objects.filter(product_configuration__product__in=products)
