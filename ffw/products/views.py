import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import  TemplateView

from models import Subcategory


class ImageView(TemplateView):


    template_name = 'image_.html'

    def get_context_data(self, **kwargs):
        context = super(ImageView, self).get_context_data(**kwargs)
        context['subs'] = Subcategory.objects.all()
        return context
