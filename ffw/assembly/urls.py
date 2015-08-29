from django.conf.urls import patterns, url

# this temporary import
from django.views.generic import TemplateView

from . import views
from products import views as product_views

urlpatterns = patterns(
    '',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^products/$', views.ProductListView.as_view(), name='products'),
    url(r'^products/(?P<section>[-\w]+)/$', views.ProductListView.as_view(), name='products'),
    url(r'^products/(?P<section>[-\w]+)/(?P<category>[-\w]+)/$', views.ProductListView.as_view(), name='products'),
    url(r'^products/(?P<section>[-\w]+)/(?P<category>[-\w]+)/(?P<subcategory>[-\w]+)/$',
        views.ProductListView.as_view(), name='products'),

    url(r'^product/(?P<product>[-\w]+)/$', views.ProductView.as_view(), name='product'),
    url(r'^comments/$', product_views.CommentListView.as_view(), name='comments'),

    # this temporary url patterns
    url(r'^static-product/$', TemplateView.as_view(template_name='static_templates/product.html')),
    url(r'^static-order/$', TemplateView.as_view(template_name='static_templates/order.html')),


)
