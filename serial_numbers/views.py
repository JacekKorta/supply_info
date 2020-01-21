from django.shortcuts import render, redirect

from .forms import ShipmentForm
from .models import Customer, Machine


def saveShippment(request):
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            form_input = form.cleaned_data
            print(form_input)
            pass
        return redirect('supply_info:index')
    else:
        form = ShipmentForm()
    return render(request, 'serial_numbers/add_shipment.html', {'form': form})
