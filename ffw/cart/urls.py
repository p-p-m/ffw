from django.conf.urls import patterns, include, url
from cart import views
from views import CartView, CartRemoveView, CartSetView, CartAddView, OrderView, ThankView


urlpatterns = patterns(
    '',
    url(r'^$', CartView.as_view(), name='cart'),
    url(r'^set/$', CartSetView.as_view(), name='cart_set'),
    url(r'^add/$', CartAddView.as_view(), name='cart_add'),
    url(r'^remove/$', CartRemoveView.as_view(), name='cart_remove'),
    url(r'^order/$', OrderView.as_view(), name='order'),
    url(r'^order/thank/$', ThankView.as_view(), name='thank'),
)
