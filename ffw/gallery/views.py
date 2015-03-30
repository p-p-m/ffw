from django.shortcuts import render
from django.views.generic import View
from gallery.models import GalleryPrimImage


class GalleryView(View):

    def get(self, request):
        prim_images = GalleryPrimImage.objects.all()
        return render(request, 'gallery/gallery.html', {'prim_images': prim_images})
