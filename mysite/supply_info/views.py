from django.shortcuts import render, redirect
from .models import ActiveProductList, PriceList, Product, ProductAvailability
from .forms import ProductFullInfoUpdateForm
from .sp_modules import receiving_data


def index(request):
    return render(request, 'supply_info/index.html', {})


def machine_list(request):
    #machines = PriceList.objects.filter(product_code__mark('M'))
    #machines = PriceList.objects.filter(product_code__mark="M")
    machines = Product.objects.prefetch_related('price_lists', 'product_availability').filter(mark='M')
    print('='*50)
    print(dir(machines[0]))
    print('-'*50)
    print(len(machines))
    print(machines[5].code)
    print(machines[5].price_lists.all())
    print(machines[5].product_availability.all()[0].availability)
    print(machines[5].product_availability.all()[0].availability_info)
    print('=' * 50)
    '''
    # Do usunięcia
    # Do zrobienia: dodać "product_availability" do machines!!!!!
    
    
    print(50*'-')
    #print(dir(machines[0].product_availability))
    print(50 * '-')
    availa = ProductAvailability.objects.raw("""
    SELECT supply_info_productavailability.*
    FROM supply_info_productavailability""")
    print(availa[0].availability_info)
    print(availa[1].availability_info)
    print(availa[2].availability_info)
    print(dir(availa[0]))'''

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