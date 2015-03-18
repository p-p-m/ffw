from products import models


def categories_processor(request):
    return {'categories': models.Category.objects.all().select_related('subcategories')}
