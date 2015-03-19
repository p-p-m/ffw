from django.conf import settings

from products import models


def categories_processor(request):
    return {'categories': models.Category.objects.filter(is_active=True).select_related('subcategories')}


def debug_processor(request):
    return {'debug': settings.DEBUG}
