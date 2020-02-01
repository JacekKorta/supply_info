from django import forms


class ProductFullInfoUpdateForm(forms.Form):
    data = forms.CharField(label='', widget=forms.Textarea)




