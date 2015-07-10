import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView

from gallery import models as gallery_models
from products import models as products_models, forms as products_forms
from . import models


# XXX: This view will be removed after product list view implementation
def filter_test_view(request):
    filters = list(models.IntervalsAttributeFilter.objects.all()[10:12])
    filters += list(models.ChoicesAttributeFilter.objects.all()[11:13])
    filters += list(models.NumericAttributeFilter.objects.all()[1:3])

    for filt in filters:
        filt.filter(products_models.Product.objects.all(), request)
    return render(request, 'assembly/filters.html', {'filters': filters})


class HomeView(View):

    def get(self, request):
        print("IP Address for debug-toolbar: " + request.META['REMOTE_ADDR'])
        main = gallery_models.Banner.objects.get(name='main')
        subcategories = products_models.Subcategory.objects.filter(is_active=True)
        return render(request, 'assembly/home.html', {'main': main, 'subcategories': subcategories})


class ProductListView(ListView):

    paginate_by = 10
    allow_empty = True

    def get(self, request, *args, **kwargs):
        if request.is_ajax() and 'count' in request.GET:
            return HttpResponse(
                json.dumps(self.get_queryset().count()),
                content_type='application/json',
            )
        return super(ProductListView, self).get(request, *args, **kwargs)

    def get_context_object_name(self, object_list):
        return 'products'

    def get_queryset(self):
        queryset = models.Product.objects.all().select_related('attributes', 'images')

        if 'subcategory' in self.kwargs:
            queryset = queryset.filter(subcategory__slug=self.kwargs['subcategory'])
        elif 'category' in self.kwargs:
            queryset = queryset.filter(subcategory__category__slug=self.kwargs['category'])
        elif 'section' in self.kwargs:
            queryset = queryset.filter(subcategory__category__section__slug=self.kwargs['section'])

        sort_form = products_forms.SortForm(self.request.GET)
        if sort_form.is_valid():
            queryset = sort_form.sort(queryset)

        filter_form = self._get_filter_form()
        if filter_form.is_valid():
            queryset = filter_form.filter_products(queryset)

        return queryset

    def get_template_names(self):
        template = super(ProductListView, self).get_template_names()[0]
        if self.request.is_ajax():
            return template[:-5] + '_table.html'
        return template

    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        key = self.__class__.__name__ + '_rows'
        if 'paginate_by' in self.request.GET:
            try:
                self.paginate_by = max(int(self.request.GET.get('paginate_by', self.paginate_by)), 5)
                self.request.session[key] = self.paginate_by
            except ValueError:
                pass
        else:
            self.paginate_by = self.request.session.get(key, self.paginate_by)
        return self.paginate_by

    def _get_selected_section(self):
        if 'section' in self.kwargs:
            try:
                return models.Section.objects.get(slug=self.kwargs['section'])
            except models.Section.DoesNotExist:
                pass

    def _get_selected_category(self):
        if 'category' in self.kwargs:
            try:
                return models.Category.objects.get(slug=self.kwargs['category'])
            except models.Category.DoesNotExist:
                pass

    def _get_selected_subcategory(self):
        if 'subcategory' in self.kwargs:
            try:
                return models.Subcategory.objects.get(slug=self.kwargs['subcategory'])
            except models.Subcategory.DoesNotExist:
                pass

    def _get_filter_form(self):
        subcategory = self._get_selected_subcategory()
        category = self._get_selected_category()
        return products_forms.FilterForm(category, subcategory, data=self.request.GET)

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['paginate_by'] = self.paginate_by
        context['total_count'] = self.get_queryset().count()
        context['sort_form'] = products_forms.SortForm(self.request.GET)
        context['filter_form'] = self._get_filter_form()

        if not self.request.is_ajax():
            context['selected_subcategory'] = self._get_selected_subcategory()
            context['selected_category'] = self._get_selected_category()
        return context


class ProductView(View):

    def get(self, request, product):
        product = get_object_or_404(models.Product.objects.select_related('attributes', 'images'), slug=product)
        return render(request, 'products/product.html', {'product': product})