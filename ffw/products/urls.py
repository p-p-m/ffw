from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^products/$', views.ProductListView.as_view(), name='products'),
    url(r'^products/(?P<category>[-\w]+)/$', views.ProductListView.as_view(), name='products'),
    url(r'^products/(?P<category>[-\w]+)/(?P<subcategory>[-\w]+)/$', views.ProductListView.as_view(), name='products'),
    url(r'^product/(?P<product>[-\w]+)/$', views.ProductView.as_view(), name='product'),
)
