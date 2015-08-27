from django.conf.urls import patterns, url
from .views import CartView, OrderView, ThankView, CartSetView, CartRemoveView, CartAddView


urlpatterns = patterns(
    '',
    url(r'^$', CartView.as_view(), name='cart'),
    url(r'^set/$', CartSetView.as_view(), name='cart_set'),
    url(r'^add/$', CartAddView.as_view(), name='cart_add'),
    url(r'^remove/$', CartRemoveView.as_view(), name='cart_remove'),
    url(r'^order/$', OrderView.as_view(), name='order'),
    url(r'^order/thank/$', ThankView.as_view(), name='thank'),
)
