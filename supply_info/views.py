from datetime import datetime

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect


from .forms import ProductFullInfoUpdateForm
from .models import Event, Product, ProductAvailability

from .sp_modules import receiving_data, db_save


def index(request):
    # this page will be changed in the future
    machines = Product.objects.prefetch_related('price_lists',
                                                'product_availability').filter(mark='M').order_by("code")
    last_update_time = Event.objects.filter(event_name='availability update').last()
    return render(request, 'supply_info/machines_list.html', {'machines': machines,
                                                             'now': datetime.today().date(),
                                                             'last_update_time': last_update_time,
                                                             })


def machines_list(request):
    machines = Product.objects.prefetch_related('price_lists',
                                                'product_availability').filter(mark='M').order_by("code")
    last_update_time = Event.objects.filter(event_name='availability update').last()
    return render(request, 'supply_info/machines_list.html', {'machines': machines,
                                                             'now': datetime.today().date(),
                                                             'last_update_time': last_update_time,
                                                             })


@login_required
def product_list(request, sub_type):
    object_list = Product.objects.prefetch_related('price_lists',
                                                'product_availability').filter(sub_type=sub_type).order_by("code")
    paginator = Paginator(object_list, 100) # 100 products per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'supply_info/products_list.html', {'products': products,
                                                              'page': page})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Twoje hasło zostało zmienione')
            db_save.event_record(request.user.username, 'password changed')
            return redirect('supply_info:change_password')
        else:
            messages.error(request, 'Bład')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'supply_info/change_password.html', {'form': form})


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
            db_save.event_record(request.user.username, 'availability update')
        return redirect('supply_info:index')
    else:
        form = ProductFullInfoUpdateForm()
    return render(request, 'supply_info/update_product_info.html', {'form': form, 'title': 'Uaktualnij stany'})


@login_required
def search_product(request):
    last_update_time = Event.objects.filter(event_name='availability update').last()
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton = request.GET.get('submit')
        if query is not None:
            lookups = Q(code__icontains=query) | Q(sub_type__icontains=query) | Q(name__icontains=query)
            results = Product.objects.prefetch_related('price_lists',
                                                       'product_availability').filter(lookups).order_by('code')
            context = {'results': results,
                       'submitbutton': submitbutton,
                       'now': datetime.today(),
                       'last_update_time': last_update_time}
            return render(request, 'supply_info/search_product.html', context)

        else:
            return render(request, 'supply_info/search_product.html')
    else:
        return render(request, 'supply_info/search_product.html')


