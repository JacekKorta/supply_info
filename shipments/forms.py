from django import forms
from django.forms import BaseFormSet
from django.forms import IntegerField

from supply_info.models import Product
from shipments.models import ShipmentDetail, Shipment


class NewShipmentDetailForm(forms.Form):
    product = forms.CharField(widget=forms.TextInput, disabled=True)
    quantity = forms.IntegerField(widget=forms.NumberInput)











