from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import Http404
from rest_framework.parsers import JSONParser # sprawdz
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import permission_classes

from .serializers import ProductSerializer, ProductAvailabilitySerializer
from .models import ActiveProductList, Event, PriceList, Product, ProductAvailability
from .forms import ProductFullInfoUpdateForm
from .sp_modules import receiving_data, db_saves


def index(request):
    # this page will be changed in the future
    machines = Product.objects.prefetch_related('price_lists', 'product_availability').filter(mark='M').order_by("code")
    last_update_time = Event.objects.filter(event_name='availability update').last()
    return render(request, 'supply_info/machine_list.html', {'machines': machines,
                                                             'now': datetime.today().date(),
                                                             'last_update_time': last_update_time,
                                                             })


def machine_list(request):
    machines = Product.objects.prefetch_related('price_lists', 'product_availability').filter(mark='M').order_by("code")
    last_update_time = Event.objects.filter(event_name='availability update').last()
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
            results = Product.objects.prefetch_related('price_lists',
                                                       'product_availability').filter(lookups).order_by('code')
            context = {'results': results,
                       'submitbutton': submitbutton,
                       'now': datetime.today()}
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


class ApiMachinesAvailabilityList(APIView):
    permission_classes = (IsAuthenticated,)
    # only machines

    def get(self, request, format=None):
        products = Product.objects.all().filter(type='maszyny')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ApiAvailabilityList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        availability = ProductAvailability.objects.all()
        serializer = ProductAvailabilitySerializer(availability, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.user.is_superuser:
            serializer = ProductAvailabilitySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ApiAvailabilityDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, product_code):
        try:
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
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)