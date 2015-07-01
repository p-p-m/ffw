from django.db import models

from product_filters.models import NumericFilterMixin


class BaseAttributeNumericFilter(NumericFilterMixin, models.Model):
    attribute_name = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def get_filter_query(self, selected_max_value, selected_min_value):
        return super(BaseAttributeNumericFilter, self).get_filter_query(
            self.attribute_name, selected_min_value, selected_max_value)


# class BaseAttributeChoicesFilter()
