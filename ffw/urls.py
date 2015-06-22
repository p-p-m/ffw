from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()


urlpatterns = patterns(
    '',
    # Custom applications
    url(r'^', include('products.urls')),
    url(r'^', include('assembly.urls')),
    url(r'^common_pages/', include('common_pages.urls')),
    url(r'^gallery/', include('gallery.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^admin/', include(admin.site.urls)),
    )


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
