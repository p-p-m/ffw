from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(
        r'^products/product/add/$',
        views.ProductCreateView.as_view(),
        name='box_admin_product_create'
    ),
    # url(
    #     r'^products/product/(?P<product_id>[0-9]+)/configuration/form/$',
    #     views.ProductConfigurationFormView.as_view(),
    #     name='box_admin_product_configuration_form',
    # ),
    # url(
    #     r'^products/product/form/$',
    #     views.ProductFormView.as_view(),
    #     name='box_admin_product_form',
    # ),
)
