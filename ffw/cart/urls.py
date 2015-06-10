from django.conf.urls import patterns, include, url
from cart import views
from views import Cart, CartRemove, CartSet

urlpatterns = patterns(
    '',
    url(r'^$', Cart.as_view(), name='cart'),
    url(r'^set/$', CartSet.as_view(), name='cart_set'),
    url(r'^remove/$', CartRemove.as_view(), name='cart_remove'),
)
