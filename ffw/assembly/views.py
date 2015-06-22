from django.shortcuts import render

from products import models as products_models
from . import models


def filter_test_view(request):
    filters = list(models.IntervalsAttributeFilter.objects.all()[10:12])
    filters += list(models.ChoicesAttributeFilter.objects.all()[11:13])
    filters += list(models.NumericAttributeFilter.objects.all()[1:3])

    for filt in filters:
        filt.filter(products_models.Product.objects.all(), request)
    return render(request, 'assembly/filters.html', {'filters': filters})
