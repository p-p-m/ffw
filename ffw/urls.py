from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

from products.views  import ImageResizeView


urlpatterns = patterns(
    '',
    # Custom applications
    url(r'^', include('assembly.urls')),
    url(r'^common_pages/', include('common_pages.urls')),
    url(r'^gallery/', include('gallery.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^image_resize', ImageResizeView.as_view(), name="image_resize"),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    # urlpatterns += patterns(
    #     '',
    #     (r'^%{static_url}/(?P<path>.*)$'.format(static_url=settings.STATIC_URL),
    #         'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    #     (r'^%{media_url}/(?P<path>.*)$'.format(media_url=settings.MEDIA_URL),
    #         'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # )
