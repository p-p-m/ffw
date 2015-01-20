import factory

from products import models


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = factory.Sequence(lambda n: 'Category #%s' % n)


class SubcategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Subcategory

    name = factory.Sequence(lambda n: 'Subcategory #%s' % n)
    category = factory.SubFactory(CategoryFactory)
