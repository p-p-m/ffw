#  -*- coding: utf-8 -*-
import json


from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View

from gallery.models import Banner
import forms
import models
from django.utils.translation import ugettext_lazy as _

from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect


class HomeView(View):

    def get(self, request):
        main = Banner.objects.get(name='main')
        subcategories = models.Subcategory.objects.filter(is_active=True)
        return render(request, 'products/home.html', {'main': main, 'subcategories': subcategories})


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

        sort_form = forms.SortForm(self.request.GET)
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
        return forms.FilterForm(category, subcategory, data=self.request.GET)

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['paginate_by'] = self.paginate_by
        context['total_count'] = self.get_queryset().count()
        context['sort_form'] = forms.SortForm(self.request.GET)
        context['filter_form'] = self._get_filter_form()

        if not self.request.is_ajax():
            context['selected_subcategory'] = self._get_selected_subcategory()
            context['selected_category'] = self._get_selected_category()
        return context


class ProductView(View):
    def get(self, request, product):
        product = get_object_or_404(models.Product.objects.select_related('attributes', 'images'), slug=product)
        return render(request, 'products/product.html', {'product': product})


@csrf_protect
def cart(request, *args, **kwargs):
    if request.is_ajax:
        if request.method == 'POST':
            c = {}
            c.update(csrf(request))

            #  data of cart in session: {'sum_cart': ..., 'count_cart': ..., 'products': {product_code1: {'name': ...,
            #  'price': ..., product_code2: {'name': ..., 'price': ...}, ....}}
            action = request.POST.get('action', '')
            request.session['products'] = request.session.get('products', {})
            request.session['sum_cart'] = 0
            request.session['count_cart'] = 0
            # if product is in the cart, msg = 'The product alredy is in the cart', else 'the product add'
            msg = ''

            #  action can be: 1 - "remove", 2 - 'clear', 3 - "add" (or any name include '' - its equal '"add")
            if action == 'clear':
                request.session['products'] = {}
                return

            # 'remove' or 'add'
            product_pk = request.POST.get('product_pk', '')
            product = get_object_or_404(models.Product.objects, pk=product_pk)
            price = float(product.price_uah)
            name = product.name

            if action == 'remove':
                del request.session['products'][product_pk]
            else:
                # action is 'add'
                if product_pk in request.session['products'].keys():
                    msg = name + ' is in the cart already'
                else:
                    msg = name + 'add in the cart'
                    request.session['products'][product_pk] = {'name': name, 'price': price}

            request.session['sum_cart'] = sum([v['price'] for v in request.session['products'].values()])
            request.session['count_cart'] = len(request.session['products'])


            return HttpResponse(json.dumps({'sum_cart': request.session['sum_cart'], 'count_cart': (
                request.session['count_cart']), 'msg': msg}), c)
