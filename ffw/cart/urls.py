from django.conf.urls import patterns, include, url
from cart import views

urlpatterns = patterns(
    '',
    url(r'^$', views.cart, name='cart'),
    url(r'^add/$', views.add, name='cart_add'),
)
