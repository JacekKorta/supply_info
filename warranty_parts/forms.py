from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Q

from serial_numbers.models import Machine
from supply_info.models import Product
from warranty_parts.models import Comments


class AddIssueForm(forms.Form):
    today = datetime.now()
    customer = forms.CharField(label='Nazwa klienta')
    machine_serial_number = forms.CharField(label='Numer seryjny maszyny')
    machine_model = forms.ModelChoiceField(queryset=Product.objects.filter(Q(mark='M') | Q(mark='0')).order_by("code"),
                                           label='Model maszyny', required=False)
    part_number = forms.CharField(label='Numer cześci')
    part_name = forms.CharField(label='Nazwa części')
    quantity = forms.IntegerField(initial=1, label='Ilość')
    issue_description = forms.CharField(widget=forms.Textarea, label='Opis usterki')
    document_number = forms.CharField(label='Numer proformy', initial=f'{today.strftime("%y")}-FP/', required=False)

    def clean(self):
        cleaned_data = super().clean()
        machine_serial_number = cleaned_data.get("machine_serial_number")
        machine_model = cleaned_data.get("machine_model")
        if machine_serial_number:
            try:
                Machine.objects.get(serial_number=machine_serial_number)
            except Machine.DoesNotExist:
                if machine_model:
                    Machine.objects.create(code=machine_model,
                                           serial_number=machine_serial_number)
                else:
                    raise forms.ValidationError(f'Maszyna o tym numerze seryjnym nie istnieje, '
                                                f'sprawdź numer lub dodaj maszynę z listy')


class AddCommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, label='Komentarz')
    inform_all = forms.BooleanField(required=False, initial=True, label='Powiadom innych')


