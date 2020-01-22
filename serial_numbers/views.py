from django.shortcuts import render, redirect

from .forms import ShipmentForm
from .models import Customer, Machine
from .sn_modules import sn_parser as snp
from .sn_modules import db_save as sndbs


def saveShippment(request):
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            form_input = form.cleaned_data
            customer = form_input['customer']
            delivery_note_number = form_input['delivery_note_number']
            shipment = snp.extract_serial_numbers(form_input['shipment'])
            machines_serials = snp.parse_serials(shipment)
            for item in machines_serials:
                sndbs.shipment_record(customer, delivery_note_number, item)
        return redirect('supply_info:index')
    else:
        form = ShipmentForm()
    return render(request, 'serial_numbers/add_shipment.html', {'form': form})
