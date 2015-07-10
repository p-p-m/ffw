from django.conf.urls import patterns, include, url

from views import ImageView

urlpatterns = patterns(
    '',
    url(r'^$', ImageView.as_view(), name='image'),

)
