# coding: utf-8
from django.forms import ModelForm, Textarea, TextInput

from models import Order


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ('name', 'email', 'phone', 'contacts')
        widgets = {
            'contacts': Textarea(attrs={'cols': 40, 'rows': 2}),
        }
