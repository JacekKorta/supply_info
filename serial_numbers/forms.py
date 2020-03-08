from django import forms

from serial_numbers.models import Customer


class ShipmentForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all().order_by('name'), label='Klient')
    delivery_note_number = forms.CharField(label='Nr dokumentu WZ (bez serii i roku):')
    shipment = forms.CharField(label='Numery seryjne', widget=forms.Textarea)


class RegisterMachineInWarehouse(forms.Form):
    """Form to register machines in warehouse.
    Data are supplied by manufacturer, few days before delivery to warehouse.
    Because registration happens before delivery date,
    the 'delivery_date' field is fill manualy.
    """

    delivery_date = forms.DateField(label='Data przyjęcia do magazynu (dd.mm.yyyy)', widget=forms.DateInput)
    machines_data = forms.CharField(label='Dane w csv', widget=forms.Textarea)