from datetime import date
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import render, redirect

from payments.forms import InvoiceDataForm
from payments.contrib import payments_mod
from payments.contrib.payments_session import Session


@staff_member_required
def read_invoices_data(request):
    if request.method == 'POST':
        form = InvoiceDataForm(request.POST)
        if form.is_valid():
            form_input = form.cleaned_data
            payments_mod.Invoice.extract_payment_data(form_input['data'])
            payments_mod.Invoice.get_delayed_invoices()
            Session.clean_payment_session(request)
            request.session['delayed_invoices'] = payments_mod.Invoice.invoices_to_dict()
        return redirect("payments:delayed_invoices")
    else:
        form = InvoiceDataForm()
    return render(request, 'payments/import_invoices_data.html', {'form': form, 'title': 'Płatności'})


@staff_member_required
def delayed_invoices_handle(request):
    delayed_invoices = request.session['delayed_invoices']
    print(delayed_invoices)
    if request.method == 'POST':
        if 'delete' in request.POST:
            Session.remove_customer(request, request.POST['delete'])

    return render(request, 'payments/delayed_payments_list.html', {'delayed_invoices': delayed_invoices})