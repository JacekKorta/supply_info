from datetime import datetime

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .forms import ProductFullInfoUpdateForm
from .models import Event, Product, ProductAvailability
from .serializers import ProductSerializer, ProductAvailabilitySerializer
from .sp_modules import receiving_data, db_saves


def index(request):
    # this page will be changed in the future
    machines = Product.objects.prefetch_related('price_lists', 'product_availability').filter(mark='M').order_by("code")
    last_update_time = Event.objects.filter(event_name='availability update').last()
    return render(request, 'supply_info/machines_list.html', {'machines': machines,
                                                             'now': datetime.today().date(),
                                                             'last_update_time': last_update_time,
                                                             })


def machines_list(request):
    machines = Product.objects.prefetch_related('price_lists', 'product_availability').filter(mark='M').order_by("code")
    last_update_time = Event.objects.filter(event_name='availability update').last()
    return render(request, 'supply_info/machines_list.html', {'machines': machines,
                                                             'now': datetime.today().date(),
                                                             'last_update_time': last_update_time,
                                                             })

def product_list(request, category):
    products = Product.objects.prefetch_related('price_lists', 'product_availability').all().order_by("code")
    print(dir(products[0]))
    return render(request, 'supply_info/products_list.html', {'products': products, 'category': category})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Twoje hasło zostało zmienione')
            db_saves.event_record(request.user.username, 'password changed')
            return redirect('supply_info:change_password')
        else:
            messages.error(request, 'Bład')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'supply_info/change_password.html', {'form':form})



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
    last_update_time = Event.objects.filter(event_name='availability update').last()
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton = request.GET.get('submit')
        if query is not None:
            lookups = Q(code__icontains=query) | Q(name__icontains=query)
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


class ApiProductList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.user.is_superuser:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ApiProductDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, code):
        try:
            code = code.replace('%20', ' ')
            return Product.objects.get(code=code)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, code, format=None):
        product = self.get_object(code)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, code, format=None):
        if request.user.is_superuser:
            product = self.get_object(code)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, code, format=None):
        if request.user.is_superuser:
            product = self.get_object(code)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ApiAvailabilityList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        availability = ProductAvailability.objects.all()
        serializer = ProductAvailabilitySerializer(availability, many=True)
        return Response(serializer.data)


class ApiAvailabilityDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, product_code):
        try:
            product_code = product_code.replace('%20', ' ')
            return ProductAvailability.objects.get(product_code=Product.objects.get(code=product_code))
        except ProductAvailability.DoesNotExist:
            raise Http404

    def get(self, request, product_code, format=None):
        availability_ob = self.get_object(product_code)
        serializer = ProductAvailabilitySerializer(availability_ob)
        return Response(serializer.data)

    def put(self, request, product_code, format=None):
        if request.user.is_superuser:
            availability_ob = self.get_object(product_code)
            serializer = ProductAvailabilitySerializer(availability_ob, data=request.data)
            if serializer.is_valid():
                serializer.save()
                db_saves.event_record(request.user.username, 'availability update')
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)