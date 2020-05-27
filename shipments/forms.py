from django import forms
from django.forms import BaseFormSet
from django.forms import IntegerField

from supply_info.models import Product
from shipments.models import ShipmentDetail, Shipment


class NewShipmentDetailForm(forms.Form):
    product = forms.CharField(widget=forms.TextInput, disabled=True)
    quantity = forms.IntegerField(widget=forms.NumberInput)


class NewShipmentForm(forms.ModelForm):
    shipment_number = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Numer dostawy'}))
    country_of_origin = forms.ChoiceField(choices=Shipment.COUNTRY_CHOICES, initial='tw')

    class Meta:
        model = Shipment
        fields = ['shipment_number', 'country_of_origin']










