from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, View

from products import models as products_models


# class ProductConfigurationFormView(CreateView):
#     template_name = 'box_admin/product_configuration_form.html'
#     model = products_models.ProductConfiguration
#     fields = ['code', 'is_active']

#     def get(self, request, product_id=None):
#         if product_id is not None:
#             self.product = get_object_or_404(products_models.Product, id=product_id)
#         return super(ProductConfigurationFormView, self).get(self, request)


class ProductCreateView(CreateView):
    template_name = 'box_admin/product_create.html'
    model = products_models.Product
    fields = ['name', 'subcategory', 'short_description', 'description', 'is_active']

    def get(self, request, product_id=None):
        if product_id is not None:
            self.product = get_object_or_404(products_models.Product, id=product_id)
        return super(ProductCreateView, self).get(self, request)

    def form_valid(self, form):
        form.save()
        return self.render_to_response(self.get_context_data(form=form))
