from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView, ListView, CreateView, FormView
from django.forms import formset_factory

from .models import Shipment, ShipmentDetail
from .forms import NewShipmentDetailForm
from supply_info.models import Product


def create_row(machines, shipments):
    rows = []
    for i in range(0, len(machines)):
        row = {'code': machines[i].code}
        quantities = []
        for shipment in shipments:
            qty = ' '
            for line in shipment.shipmentdetail_set.values():
                if line.get('product_id', ' ') == machines[i].id:
                    qty = line['quantity']
            quantities.append(qty)
        row['quantities'] = quantities
        qty_sum = sum([x for x in row['quantities'] if type(x) == int])
        row['qty_sum'] = qty_sum
        rows.append(row)
    return rows


@staff_member_required
def shipments_view(request):
    today = datetime.now().date()
    machines = Product.objects.filter(mark='M').order_by("code")
    shipments = Shipment.objects.select_related().\
        exclude(estimated_time_arrival__lt=today).\
        exclude(shipment_status__in=['done', 'canceled']).order_by('estimated_time_arrival')
    rows = create_row(machines, shipments)
    return render(request, 'shipments/shipments_list.html', {'shipments': shipments,
                                                             'machines': machines,
                                                             'rows': rows})


@staff_member_required
def add_new_shipment(request):
    machines = Product.objects.filter(mark='M').order_by("code")
    NewShipmentFormset = formset_factory(NewShipmentDetailForm, max_num=len(machines))
    if request.method == 'POST':
        formset = NewShipmentFormset(request.POST, initial=[{'product': machine.code, 'quantity': 0} for machine in machines])
        if formset.is_valid():
            formset_input = formset.cleaned_data
            shipment_number = Shipment.form_unique_name_validation(request.POST['shipment_number'])
            shipment = Shipment.objects.create(shipment_number=shipment_number)
            for item in formset_input:
                if item['quantity'] > 0:
                    product = Product.objects.get(code=item['product'])
                    ShipmentDetail.objects.create(shipment=shipment,
                                                  product=product,
                                                  quantity=item['quantity'])

        return redirect('shipments:shipments_view')
    else:
        formset = NewShipmentFormset(initial=[{'product': machine.code, 'quantity': 0} for machine in machines])

    context = {'machines': machines,
               'formset': formset
               }
    return render(request, 'shipments/new_shipment_form.html', context)







"""
form_class = NewShipmentDetailForm
template_name = 'shipments/new_shipment_form.html'
form = NewShipmentDetailForm
success_url = '/dostawy/nowa'

def get_context_data(self, **kwargs):
    machines = Product.objects.filter(mark='M').order_by("code")
    formset = formset_factory(NewShipmentDetailForm, max_num=len(machines))
    context = {'machines': machines,
               'formset': formset(initial=[{'product':machine.code, 'quantity':0} for machine in machines])
               }
    return context

def form_valid(self, formset):
    print(formset.cleaned_data)
    def post(self, request, *args, **kwargs):
    """



