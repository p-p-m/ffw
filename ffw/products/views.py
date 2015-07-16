#  -*- coding: utf-8 -*-

from django.views.generic import TemplateView

from models import Subcategory



class ImageResizeView(TemplateView):

    template_name = 'image_resize.html'

    def get_context_data(self, **kwargs):
        context = super(ImageResizeView, self).get_context_data(**kwargs)
        context['subcategories'] = Subcategory.objects.all()
        return context