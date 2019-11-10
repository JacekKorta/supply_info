from django import forms

from .models import Product


class ProductFullInfoUpdateForm(forms.Form):
    data = forms.CharField(label='', widget=forms.Textarea)



