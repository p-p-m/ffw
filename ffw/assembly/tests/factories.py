import factory

from products.tests import factories as products_factories
from .. import models


class BaseAttributeFilterFactory(factory.DjangoModelFactory):
    ABSTRACT_FACTORY = True

    subcategory = factory.SubFactory(products_factories.SubcategoryFactory)
    characteristic = factory.SubFactory(products_factories.CharacteristicFactory)


class ChoicesAttributeFilterFactory(BaseAttributeFilterFactory):
    class Meta:
        model = models.ChoicesAttributeFilter

    choices = factory.Iterator(['1, 2, 3, 4', 'a, b, c, d', 'qwer, tyui, asdf, zxcv'])
    priority = factory.Sequence(lambda i: i)
    name = factory.Sequence(lambda i: 'Filter #{}'.format(i))


class IntervalAttributeFilterFactory(BaseAttributeFilterFactory):
    class Meta:
        model = models.IntervalsAttributeFilter

    intervals = factory.Iterator(['0-10, 10-20, 20-30', '0-100, 100-200, 200-300', '0-1, 1-2, 2-3, 3-4'])
    priority = factory.Sequence(lambda i: i)
    name = factory.Sequence(lambda i: 'Filter #{}'.format(i))


class NumericAttributeFilterFactory(BaseAttributeFilterFactory):
    class Meta:
        model = models.NumericAttributeFilter

    max_value = 1000
    min_value = 0
    priority = factory.Sequence(lambda i: i)
    name = factory.Sequence(lambda i: 'Filter #{}'.format(i))
