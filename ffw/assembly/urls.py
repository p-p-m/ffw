from django.conf.urls import patterns, url


from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^products/$', views.ProductListView.as_view(), name='products'),
    url(r'^products/(?P<section>[-\w]+)/$', views.ProductListView.as_view(), name='products'),
    url(r'^products/(?P<section>[-\w]+)/(?P<category>[-\w]+)/$', views.ProductListView.as_view(), name='products'),
    url(r'^products/(?P<section>[-\w]+)/(?P<category>[-\w]+)/(?P<subcategory>[-\w]+)/$',
        views.ProductListView.as_view(), name='products'),

    url(r'^product/(?P<product>[-\w]+)/$', views.ProductView.as_view(), name='product'),
)
