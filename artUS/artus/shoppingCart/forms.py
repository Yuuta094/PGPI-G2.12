from django import forms
from core.models import Customer

WIDGETS_STILES= 'w-full py-2 px-2 rounded-xl border'

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['address', 'country', 'city', 'zip_code', 'telephone']

        widgets = {
            'address': forms.Textarea(attrs={
            'class': WIDGETS_STILES
        }),
            'country': forms.TextInput(attrs={
            'class': WIDGETS_STILES
        }),
            'city': forms.TextInput(attrs={
            'class': WIDGETS_STILES
        }),
            'zip_code': forms.TextInput(attrs={
            'class': WIDGETS_STILES
        }),
            'telephone': forms.TextInput(attrs={
            'class': WIDGETS_STILES
        }),
        }