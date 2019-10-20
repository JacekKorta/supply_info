from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductFullInfoUpdateForm


def index(request):
    return render(request, 'supply_info/index.html', {})


def machine_list(request):
    return render(request, 'supply_info/machine_list.html', {})


def update_product_info(request):
    if request.method == 'POST':
        form = ProductFullInfoUpdateForm(request.POST)
        if form.is_valid():
            form_input = form.cleaned_data

            for line in form_input['data'].split('\n'):
                print(line) #rozpakuj        #a,b =line.split('\t') + czyszczenie #
        return redirect('supply_info:index')
    else:
        form = ProductFullInfoUpdateForm()
    return render(request, 'supply_info/update_product_info.html', {'form': form})