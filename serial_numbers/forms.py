from django import forms
from .models import Customer


class ShipmentForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all().order_by('name'), label='Klient')
    delivery_note_number = forms.CharField(label='Nr dokumentu WZ')
    shipment = forms.CharField(label='Numery seryjne', widget=forms.Textarea)