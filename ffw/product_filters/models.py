from __future__ import unicode_literals

from django.db import models


class FilterTypes(object):
    NUMERIC = 'numeric'
    CHOICES = 'choices'
    INTERVALS = 'intervals'


# XXX: This filter is not general. It cannot handle ProductAttribute model right
class FilterMixin(object):
    name = models.CharField(max_length=50)
    priority = models.FloatField('Priority', help_text='Filters with higher priority are displayed higher on page')
    is_manually_edited = models.BooleanField(default=False)
    filtered_attribute_name = models.CharField(max_length=50)

    def get_queryset(self):
        raise NotImplemented()

    def filter(self, *args, **kwargs):
        return self.get_queryset().filter(self.get_filter_query(self.filtered_attribute_name, *args, **kwargs))

    def get_filter_query(self, field, **kwargs):
        raise NotImplemented()

    def get_type(self):
        raise NotImplemented()

    def update(self):
        if self.is_manually_edited:
            return
        self.base_update(self.filtered_attribute_name)

    def base_update(self, field):
        raise NotImplemented()


class NumericFilterMixin(FilterMixin):
    """
    Abstract numeric filter mixin
    """
    max_value = models.FloatField('Max')
    min_value = models.FloatField('Min')

    def get_type(self):
        return FilterTypes.NUMERIC

    def get_filter_query(self, field, selected_min_value, selected_max_value):
        return models.Q(**{
            '{}__gte'.format(field): selected_min_value,
            '{}__lte'.format(field): selected_max_value})

    def base_update(self, field):
        max_and_min = self.get_queryset().aggregate(models.Max(field), models.Min(field))
        new_max_value = max_and_min['{}__max'.format(field)]
        new_min_value = max_and_min['{}__min'.format(field)]
        if self.min_value != new_min_value or self.max_value != new_max_value:
            self.min_value = new_min_value
            self.max_value = new_max_value
            self.save()


class ChoicesFilterMixin(FilterMixin):
    """
    Abstract choices filter mixin
    """
    choices = models.TextField('Choices', help_text='Comma-separated list of choices')

    def get_type(self):
        return FilterTypes.CHOICES

    def get_formatted_choices(self):
        return [choice.strip() for choice in self.choices.split(',')]

    def get_filter_query(self, field, choices):
        return models.Q(**{'{}__in'.format(field): choices})


class IntervalsFilterMixin(FilterMixin):
    """
    Abstract intervals filter mixin
    """
    intervals = models.TextField(
        'Intervals', help_text='Comma-separated list of intervals. Example: 0-100, 100-200 ...')

    def get_type(self):
        return FilterTypes.INTERVALS

    def get_formatted_intervals(self):
        intervals = [interval.strip() for interval in self.intervals.split(',')]
        return [(float(i.split('-')[0].strip()), float(i.split('-'))[1].strip()) for i in intervals]

    def get_filter_query(self, field, intervals):
        query = models.Q()
        for min_value, max_value in intervals:
            query |= models.Q(**{'{}__gte'.format(field): min_value, '{}__lte'.format(field): max_value})
