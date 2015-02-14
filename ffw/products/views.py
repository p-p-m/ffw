from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from gallery.models import Banner
import forms
import models


class HomeView(View):

    def get(self, request):
        categories = models.Category.objects.all().select_related('subcategories')
        top =  Banner.objects.get(name='top')
        main = Banner.objects.get(name='main')       
        images = main.images.all()
        return render(request, 'products/home.html', {'categories': categories,
                      'top': top, 'main': main})


class ProductListView(ListView):

    paginate_by = 10
    allow_empty = True

    def get_context_object_name(self, object_list):
        return 'products'

    def get_queryset(self):
        queryset = models.Product.objects.all().select_related('attributes', 'images')

        if 'subcategory' in self.kwargs:
            queryset = queryset.filter(subcategory__slug=self.kwargs['subcategory'])
        elif 'category' in self.kwargs:
            queryset = queryset.filter(subcategory__category__slug=self.kwargs['category'])

        sort_form = forms.SortForm(self.request.GET)
        if sort_form.is_valid():
            queryset = sort_form.sort(queryset)

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

    def _get_selected_category(self):
        if 'category' in self.kwargs:
            try:
                return models.Category.objects.get(slug=self.kwargs['category'])
            except models.Category.DoesNotExist:
                pass

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['paginate_by'] = self.paginate_by
        context['total_count'] = self.get_queryset().count()
        if not self.request.is_ajax():
            context['categories'] = models.Category.objects.all().select_related('subcategories')
            context['selected_category'] = self._get_selected_category()
        return context


class ProductView(View):

    def get(self, request, product):
        product = get_object_or_404(models.Product.objects.select_related('attributes', 'images'), slug=product)
        return render(request, 'products/product.html', {'product': product})
