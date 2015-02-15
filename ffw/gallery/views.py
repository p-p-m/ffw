from django.shortcuts import  render  #get_object_or_404,
#from django.http import HttpResponseRedirect
#from django.core.urlresolvers import reverse
from django.views.generic import View
from gallery.models import GalleryPrimImage


class GalleryView(View):

    def get(self, request):
        prim_images = GalleryPrimImage.objects.all()
        return render(request, 'gallery/gallery.html', {'prim_images': prim_images})
