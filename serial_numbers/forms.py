from django import forms
from .models import Customer


class ShipmentForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), empty_label=None)
    # customer = forms.CharField(label='Nazwa klienta')
    shipment = forms.CharField(label='Numery seryjne', widget=forms.Textarea)