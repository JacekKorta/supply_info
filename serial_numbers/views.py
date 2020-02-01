from datetime import date
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect


from .forms import ShipmentForm, RegisterMachineInWarehouse
from .sn_modules import sn_parser as snp
from .sn_modules import db_save as sndbs


@staff_member_required
def save_shipment(request):
    today = date.today()
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            form_input = form.cleaned_data
            customer = form_input['customer']
            delivery_note_number = f"WZ/{form_input['delivery_note_number']}/{today.year}"
            shipment = snp.extract_serial_numbers(form_input['shipment'])
            machines_serials = snp.parse_serials(shipment)
            for item in machines_serials:
                sndbs.shipment_record(customer, delivery_note_number, item)
        return redirect('serial_numbers:save_shipment')
    else:
        form = ShipmentForm()
    return render(request, 'serial_numbers/add_shipment.html', {'form': form,
                                                                'date_year': today.year})


@staff_member_required
def register_machines_in_warehouse(request):
    if request.method == 'POST':
        form = RegisterMachineInWarehouse(request.POST)
        if form.is_valid():
            form_input = form.cleaned_data
            delivery_date = form_input['delivery_date']
            machines = snp.extract_data_to_register_machine(form_input['machines_data'])
            for code, serial_number in machines:
                sndbs.save_delivery(serial_number, code, delivery_date)
        return redirect('serial_numbers:register_machines_in_warehouse')
    else:
        form = RegisterMachineInWarehouse()
    return render(request, 'serial_numbers/register_machines.html', {'form': form})



