from decimal import Decimal

import factory
import factory.fuzzy

from .. import models


class SectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Section

    name = factory.Sequence(lambda n: 'Section #%s' % n)
    slug = factory.Sequence(lambda n: 'section-%s' % n)


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = factory.Sequence(lambda n: 'Category #%s' % n)
    slug = factory.Sequence(lambda n: 'category-%s' % n)
    section = factory.SubFactory(SectionFactory)


class SubcategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Subcategory

    name = factory.Sequence(lambda n: 'Subcategory #%s' % n)
    slug = factory.Sequence(lambda n: 'subcategory-%s' % n)
    category = factory.SubFactory(CategoryFactory)


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.Sequence(lambda n: 'Product #%s' % n)
    slug = factory.Sequence(lambda n: 'Product-%s' % n)
    code = factory.Sequence(lambda n: 'Product-code-%s' % n)
    subcategory = factory.SubFactory(SubcategoryFactory)

    price_uah = factory.fuzzy.FuzzyDecimal(low=1000, high=20000)
    price_usd = factory.LazyAttribute(lambda product: product.price_uah / Decimal(20.0))
    price_eur = factory.LazyAttribute(lambda product: product.price_uah / Decimal(24.0))

    short_description = factory.Sequence(lambda n: 'Short description for Product #%s' % n)
    description = factory.Sequence(lambda n: 'Description for Product #%s' % n)

    rating = factory.fuzzy.FuzzyFloat(low=0.0, high=5.0)

    @factory.post_generation
    def additional_attributes(self, create, extracted, **kwargs):
        if create:
            if extracted:
                for attribute in extracted:
                    self.attributes.add(attribute)
            else:
                for name in ['Color', 'Width', 'Height']:
                    self.attributes.add(ProductAttributeFactory(product=self, name=name))


class ProductAttributeFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.ProductAttribute

    product = factory.SubFactory(ProductFactory)
    name = factory.Sequence(lambda n: 'Attribute #%s' % n)
    value = factory.Sequence(lambda n: n)


class CharacteristicFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Characteristic

    name = factory.Sequence(lambda n: 'Characteristic #%s' % n)
    units = factory.Iterator(['mm', 'cm', 'kg', 'g'])
