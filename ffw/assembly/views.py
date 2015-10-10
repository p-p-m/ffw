# coding: utf-8
import json

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView

from gallery import models as gallery_models
from products import models as products_models, forms as products_forms
from . import models


class HomeView(View):

    def get(self, request):
        main = gallery_models.Banner.objects.get(name='main')
        subcategories = products_models.Subcategory.objects.filter(is_active=True)
        return render(request, 'assembly/home.html', {'main': main, 'subcategories': subcategories})


class ProductListView(ListView):

    paginate_by = 12
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
        queryset = products_models.Product.objects.filter(is_active=True).select_related('images')

        self.filters = []
        if 'subcategory' in self.kwargs:
            subcategory = get_object_or_404(products_models.Subcategory, slug=self.kwargs['subcategory'])
            queryset = queryset.filter(subcategory=subcategory)
            self.filters += models.get_subcategory_filters(subcategory)
        elif 'category' in self.kwargs:
            category = get_object_or_404(products_models.Category, slug=self.kwargs['category'])
            queryset = queryset.filter(subcategory__category=category)
            self.filters += models.get_category_filters(category)
        elif 'section' in self.kwargs:
            section = get_object_or_404(products_models.Section, slug=self.kwargs['section'])
            queryset = queryset.filter(subcategory__category__section__slug=self.kwargs['section'])
            self.filters += models.get_section_filters(section)

        configurations_queryset = products_models.ProductConfiguration.objects.all()
        for filt in self.filters:
            configurations_queryset = filt.filter(configurations_queryset, self.request)

        self.filters = sorted(self.filters, key=lambda f: f.priority, reverse=True)

        queryset = queryset.filter(configurations=configurations_queryset).distinct()

        sort_form = products_forms.SortForm(self.request.GET)
        if sort_form.is_valid():
            queryset = sort_form.sort(queryset)
        else:
            queryset = queryset.annotate(null_price=Count('price_min')).order_by('-null_price', '-rating')

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
                return products_models.Section.objects.get(slug=self.kwargs['section'])
            except models.Section.DoesNotExist:
                pass

    def _get_selected_category(self):
        if 'category' in self.kwargs:
            try:
                return products_models.Category.objects.get(slug=self.kwargs['category'])
            except models.Category.DoesNotExist:
                pass

    def _get_selected_subcategory(self):
        if 'subcategory' in self.kwargs:
            try:
                return products_models.Subcategory.objects.get(slug=self.kwargs['subcategory'])
            except models.Subcategory.DoesNotExist:
                pass

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['paginate_by'] = self.paginate_by
        context['total_count'] = self.get_queryset().count()
        context['sort_form'] = products_forms.SortForm(self.request.GET)
        context['filters'] = self.filters
        context['view_type'] = self.request.GET.get('view_type', 'list')

        if not self.request.is_ajax():
            context['selected_subcategory'] = self._get_selected_subcategory()
            context['selected_category'] = self._get_selected_category()
            context['selected_section'] = self._get_selected_section()
        return context


class ProductView(View):

    def get(self, request, product):
        product = get_object_or_404(products_models.Product.objects.select_related('images'), slug=product)
        if not request.is_ajax():
            return render(request, 'products/product.html', {'product': product})
        else:
            return render(request, 'products/product_buy_popup.html', {'product': product})
