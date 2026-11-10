from django import forms

from .models import Payment, Sale


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('customer', 'discount', 'payment_method', 'status')
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('amount', 'method', 'reference')
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'method': forms.Select(attrs={'class': 'form-select'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
        }
