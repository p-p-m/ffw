from django.conf.urls import patterns, include, url
from cart import views
from views import CartView, CartRemoveView, CartSetView, CartTestView

urlpatterns = patterns(
    '',
    url(r'^test/$', CartTestView.as_view(), name='cart_test'),
    url(r'^$', CartView.as_view(), name='cart'),
    url(r'^set/$', CartSetView.as_view(), name='cart_set'),
    url(r'^remove/$', CartRemoveView.as_view(), name='cart_remove'),
)
