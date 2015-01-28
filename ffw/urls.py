from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns(
    '',
    # Custom applications
    url(r'^', include('products.urls')),
    url(r'^common_pages/', include('common_pages.urls')),


    url(r'^admin/', include(admin.site.urls)),
)
