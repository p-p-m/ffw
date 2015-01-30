from django.shortcuts import get_object_or_404,render

from django.http import HttpResponse, Http404
from common_pages.models import StaticPage

def pageListGet(request):
    pageList=StaticPage.objects.all().order_by('-created')
    context={'pageList':pageList}
    return render(request,'common_pages/index.html',context)
    
def pageGet(request,slug):
    try:
        page=StaticPage.objects.get(slug=slug)
    except StaticPage.DoesNotExist:
        raise Http404("Page does not exist")
    
    return HttpResponse(page) 



