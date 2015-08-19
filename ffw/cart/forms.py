# coding: utf-8
from django.forms import ModelForm, Textarea, TextInput

from models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('name', 'email', 'telefone', 'contacts', 'quant', 'total')
        widgets = {
            'contacts': Textarea(attrs={'cols': 40, 'rows': 2}),
            'quant': TextInput(attrs={'disabled': 'disabled', 'data-role': 'id_quant'}),
            'total': TextInput(attrs={'disabled': 'disabled', 'data-role': 'id_total'}),
        }
