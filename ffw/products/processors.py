from django.conf import settings

from products import models


def categories_processor(request):
    sections = models.Section.objects.filter(is_active=True).select_related('categories', 'categories__subcategories')
    return {
        'sections': sections,
    }


def debug_processor(request):
    return {'debug': settings.DEBUG}
