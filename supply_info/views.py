from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import  staff_member_required
from django.shortcuts import render, redirect
from django.db.models import Q
from datetime import datetime

from .models import ActiveProductList, Event, PriceList, Product, ProductAvailability
from .forms import ProductFullInfoUpdateForm
from .sp_modules import receiving_data, db_saves



def index(request):
    # this page will be changed in the future
    machines = Product.objects.prefetch_related('price_lists', 'product_availability').filter(mark='M').order_by("code")
    last_update_time = Event.objects.filter(event_name='availability update').first()
    return render(request, 'supply_info/machine_list.html', {'machines': machines,
                                                             'now': datetime.today().date(),
                                                             'last_update_time': last_update_time,
                                                             })


def machine_list(request):
    machines = Product.objects.prefetch_related('price_lists', 'product_availability').filter(mark='M').order_by("code")
    last_update_time = Event.objects.filter(event_name='availability update').first()
    return render(request, 'supply_info/machine_list.html', {'machines': machines,
                                                             'now': datetime.today().date(),
                                                             'last_update_time': last_update_time,
                                                             })



@staff_member_required
def update_product_info(request):
    if request.method == 'POST':
        form = ProductFullInfoUpdateForm(request.POST)
        if form.is_valid():
            form_input = form.cleaned_data
            receiving_data.receive_main_data(form_input['data'])
        return redirect('supply_info:index')
    else:
        form = ProductFullInfoUpdateForm()
    return render(request, 'supply_info/update_product_info.html', {'form': form, 'title': 'Import produktów'})


@staff_member_required
def update_product_availability(request):
    if request.method == 'POST':
        form = ProductFullInfoUpdateForm(request.POST)
        if form.is_valid():
            form_input = form.cleaned_data
            receiving_data.receive_availability_data(form_input['data'])
            db_saves.event_record(request.user.username, 'availability update')
        return redirect('supply_info:index')
    else:
        form = ProductFullInfoUpdateForm()
    return render(request, 'supply_info/update_product_info.html', {'form': form, 'title': 'Uaktualnij stany'})


@login_required
def search_product(request):
    if request.method == 'GET':

        query = request.GET.get('q')
        submitbutton = request.GET.get('submit')
        if query is not None:
            lookups = Q(code__icontains=query) | Q(name__icontains=query)
            results = Product.objects.prefetch_related('price_lists', 'product_availability').filter(lookups).order_by('code')
            context = {'results': results,
                       'submitbutton':submitbutton,
                       'now': datetime.today()}
            return render(request, 'supply_info/search_product.html', context)

        else:
            return render(request, 'supply_info/search_product.html')
    else:
        return render(request, 'supply_info/search_product.html')

