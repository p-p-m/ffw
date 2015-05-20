from django.conf.urls import patterns, include, url
from cart import views

urlpatterns = patterns(
    '',
    url( r'^$', views.cart, name='cart' ),
    url( r'^set/$', views.set, name='cart_set' ),
    url( r'^remove/$', views.remove, name='cart_remove' ),
)
