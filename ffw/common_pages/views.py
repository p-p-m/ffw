from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from common_pages.models import StaticPage

def index(request):
    
    #myObj=Staticpage.objects.(slug=
    return HttpResponse("Hello, world. You're at the common_pages index.")

def article(request,slug):
    myObj=StaticPage.objects.get(slug='aaaa')
    
    return HttpResponse("Article - " + myObj.text)



