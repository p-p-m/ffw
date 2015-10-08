from django import forms
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from . import models


class SortForm(forms.Form):
    SORT_CHOICES = (
        ('PA', _('Price, from small to big')),
        ('PD', _('Price, from big to small')),
    )

    sort_by = forms.ChoiceField(choices=SORT_CHOICES)

    def sort(self, queryset):
        sort_by = self.cleaned_data['sort_by']
        if sort_by == 'PA':
            queryset = queryset.annotate(null_price=Count('price_min')).order_by('-null_price', 'price_min')
        elif sort_by == 'PD':
            queryset = queryset.order_by('-price_max')
        return queryset


class CommentForm(forms.ModelForm):

    class Meta(object):
        model = models.Comment
        fields = ('username', 'comments', 'positive_sides', 'negative_sides', 'product')
