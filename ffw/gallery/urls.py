from django.conf.urls import patterns, include, url
from gallery import views

urlpatterns = patterns(
    '',
    url(r'^$', views.GalleryView.as_view(), name='gallery'),
)
