from django import forms


class InvoiceDataForm(forms.Form):
    data = forms.CharField(label='Tu wklej dane z symfonii', widget=forms.Textarea)