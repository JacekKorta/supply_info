from django.shortcuts import render, redirect
from .models import PriceList, Product
from .forms import ProductFullInfoUpdateForm
from .sp_modules import receiving_data


def index(request):
    return render(request, 'supply_info/index.html', {})


def machine_list(request):
    machines = PriceList.objects.filter(product_code__mark='M')

    return render(request, 'supply_info/machine_list.html', {'machines': machines})


def update_product_info(request):
    if request.method == 'POST':
        form = ProductFullInfoUpdateForm(request.POST)
        if form.is_valid():
            form_input = form.cleaned_data
            receiving_data.receive_main_data(form_input['data'])
            """for line in form_input['data'].split('\n'):
                print(len(line.split('\t')))  # rozpakuj        #a,b =line.split('\t') + czyszczenie #"""
        return redirect('supply_info:index')
    else:
        form = ProductFullInfoUpdateForm()
    return render(request, 'supply_info/update_product_info.html', {'form': form})