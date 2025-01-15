from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import DateInput

from .models import Contract, FinanceDetails, WarrantyCase


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['number', 'lessee', 'seller', 'meter', 'started']
        widgets = {
            'started': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lessee'].queryset = User.objects.filter(profile__role='LE')
        self.fields['lessee'].label_from_instance = lambda obj: str(obj.profile)
        self.fields['seller'].queryset = User.objects.filter(profile__role='SE')
        self.fields['seller'].label_from_instance = lambda obj: str(obj.profile)


class FinanceDetailsForm(forms.ModelForm):
    class Meta:
        model = FinanceDetails
        fields = ['cost', 'upfront', 'final_payment', 'period', 'rate', 'vat_rate']


class WarrantyCaseForm(forms.ModelForm):
    class Meta:
        model = WarrantyCase
        fields = ['contract', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['contract'].queryset = Contract.objects.filter(lessee=self.user)
            self.fields['contract'].label_from_instance = lambda obj: str(obj)
