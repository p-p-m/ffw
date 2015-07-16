from django import forms
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _


class SortForm(forms.Form):
    SORT_CHOICES = (
        ('PA', _('Price, from small to big')),
        ('PD', _('Price, from big to small')),
        ('RD', _('Rating, from big to small')),
    )

    sort_by = forms.ChoiceField(choices=SORT_CHOICES)

    def sort(self, queryset):
        sort_by = self.cleaned_data['sort_by']
        if sort_by == 'PA':
            queryset = queryset.annotate(null_price=Count('price_uah')).order_by('-null_price', 'price_uah')
        elif sort_by == 'PD':
            queryset = queryset.order_by('-price_uah')
        elif sort_by == 'RD':
            queryset = queryset.order_by('-rating')
        return queryset
