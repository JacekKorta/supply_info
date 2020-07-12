from django import forms

from supply_info.models import Alert


class ProductFullInfoUpdateForm(forms.Form):
    data = forms.CharField(label='', widget=forms.Textarea)


class AlertEditForm(forms.ModelForm):
    LESS_EQUAL_CHOICES = (
        (True, 'Mniej lub równe'),
        (False, 'Więcej niż')
    )
    less_or_equal = forms.ChoiceField(choices=LESS_EQUAL_CHOICES, initial=True,
                                      label='Opcja', widget=forms.Select())
    qty_alert_lvl = forms.IntegerField(required=True, widget=forms.NumberInput, label='Poziom alertu (szt.)')
    is_active = forms.BooleanField(label='Aktywny', required=False)

    class Meta:
        model = Alert
        fields = ['less_or_equal', 'qty_alert_lvl', 'is_active']




