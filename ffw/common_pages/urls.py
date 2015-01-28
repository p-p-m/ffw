from django.conf.urls import patterns, url

from common_pages import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<slug>\w+)/$',views.article,name='slug'),
)
