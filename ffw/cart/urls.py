from django.conf.urls import patterns, include, url
from cart import views
from views import CartView, CartRemoveView, CartSetView, CartTestView, CartAddView, CartOrderView

urlpatterns = patterns(
    '',
    url(r'^test/$', CartTestView.as_view(), name='cart_test'),
    url(r'^$', CartView.as_view(), name='cart'),
    url(r'^set/$', CartSetView.as_view(), name='cart_set'),
    url(r'^add/$', CartAddView.as_view(), name='cart_add'),
    url(r'^remove/$', CartRemoveView.as_view(), name='cart_remove'),
    url(r'^order/$', CartOrderView.as_view(), name='cart_order'),
)
