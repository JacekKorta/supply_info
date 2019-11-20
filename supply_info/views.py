from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q

from .models import ActiveProductList, PriceList, Product, ProductAvailability
from .forms import ProductFullInfoUpdateForm
from .sp_modules import receiving_data


def index(request):
    machines = Product.objects.prefetch_related('price_lists', 'product_availability').filter(mark='M').order_by("code")

    return render(request, 'supply_info/machine_list.html', {'machines': machines})


def machine_list(request):
    machines = Product.objects.prefetch_related('price_lists', 'product_availability').filter(mark='M').order_by("code")

    return render(request, 'supply_info/machine_list.html', {'machines': machines})



@login_required
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


@login_required
def update_product_availability(request):
    if request.method == 'POST':
        form = ProductFullInfoUpdateForm(request.POST)
        if form.is_valid():
            form_input = form.cleaned_data
            receiving_data.receive_availability_data(form_input['data'])
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
                       'submitbutton':submitbutton}
            return render(request, 'supply_info/search_product.html', context)

        else:
            return render(request, 'supply_info/search_product.html')
    else:
        return render(request, 'supply_info/search_product.html')