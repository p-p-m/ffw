from django.db import models


class NotDefaultManager(models.Manager):

    def get_queryset(self):
        return super(NotDefaultManager, self).get_queryset().filter(is_default=False)

    def get_origin_queryset(self):
        return super(NotDefaultManager, self).get_queryset()
