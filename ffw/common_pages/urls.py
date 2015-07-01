from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^$', views.page_list_get, name='page_list'),
    url(r'^(?P<slug>[-\w]+)/$', views.page_get, name='page'),
)
