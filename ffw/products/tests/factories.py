from decimal import Decimal

import factory
import factory.fuzzy

from products import models


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = factory.Sequence(lambda n: 'Category #%s' % n)
    slug = factory.Sequence(lambda n: 'category-%s' % n)


class SubcategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Subcategory

    name = factory.Sequence(lambda n: 'Subcategory #%s' % n)
    slug = factory.Sequence(lambda n: 'Subcategory-%s' % n)
    category = factory.SubFactory(CategoryFactory)


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.Sequence(lambda n: 'Product #%s' % n)
    slug = factory.Sequence(lambda n: 'Product-%s' % n)
    code = factory.Sequence(lambda n: 'Product-code-%s' % n)
    subcategory = factory.SubFactory(SubcategoryFactory)

    price_uah = factory.fuzzy.FuzzyDecimal(low=10000, high=200000)
    price_usd = factory.LazyAttribute(lambda product: product.price_uah / Decimal(20.0))
    price_eur = factory.LazyAttribute(lambda product: product.price_uah / Decimal(24.0))

    short_description = factory.Sequence(lambda n: 'Short description for Product #%s' % n)
    description = factory.Sequence(lambda n: 'Description for Product #%s' % n)

    @factory.post_generation
    def additional_attributes(self, create, extracted, **kwargs):
        if create:
            if extracted:
                for attribute in extracted:
                    self.attributes.add(attribute)
            else:
                for _ in range(3):
                    self.attributes.add(ProductAttributeFactory(product=self))


class ProductAttributeFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.ProductAttribute

    product = factory.SubFactory(ProductFactory)
    name = factory.Sequence(lambda n: 'Attribute #%s' % n)
    value = factory.Sequence(lambda n: n)
