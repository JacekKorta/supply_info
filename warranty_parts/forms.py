from django import forms

from serial_numbers.models import Machine


class AddIssueForm(forms.Form):
    customer = forms.CharField(label='Nazwa klienta')
    machine_serial_number = forms.CharField(label='Numer seryjny maszyny')
    part_number = forms.CharField(label='Numer cześci')
    part_name = forms.CharField(label='Nazwa części')
    quantity = forms.IntegerField(initial=1, label='Ilość')
    issue_description = forms.CharField(widget=forms.Textarea, label='Opis usterki')
    document_number = forms.CharField(label='Numer proformy', required=False)

    def clean_machine_serial_number(self):
        serial_number = self.cleaned_data['machine_serial_number']
        if Machine.objects.filter(serial_number=serial_number).all() is None:
            raise forms.ValidationError('Podana maszyna nie figuruje w bazie')
        return serial_number