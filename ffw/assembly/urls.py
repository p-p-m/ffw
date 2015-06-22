from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^test/$', views.filter_test_view, name='test'),
)
