from django.db import models


class ProductFilterManager(models.Manager):

    def for_product(self, product):
        query = (
            models.Q(section=product.subcategory.category.section) |
            models.Q(category=product.subcategory.category) |
            models.Q(subcategory=product.subcategory)
        )
        return self.get_queryset().filter(query)
