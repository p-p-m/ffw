from django.shortcuts import get_object_or_404,render, get_list_or_404

from django.http import HttpResponse, Http404
from common_pages.models import StaticPage

def page_list_get(request):
    page_list = get_list_or_404(StaticPage.objects.all().order_by('-created'))
    context = {'page_list' : page_list}
    return render(request, 'common_pages/page_list.html', context)
    
def page_get(request,slug):    
    page = get_object_or_404(StaticPage.objects, slug = slug)
    context = {'page' : page}
    return render(request,'common_pages/page.html',context) 
 


