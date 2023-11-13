from django import forms
from .models import Obra

WIDGETS_STILES= 'w-full py-4 px-6 rounded-xl border'

class EdititemForm(forms.ModelForm):
    class Meta:
        model= Obra
        fields= ('nombre','descripción','precio', 'imagen','is_sold')
        
        widgets = {
            'nombre': forms.Textarea(attrs={
                'class': WIDGETS_STILES
            }),
            'descripcion': forms.Textarea(attrs={
                'class': WIDGETS_STILES
            }),
            'precio': forms.TextInput(attrs={
                'class': WIDGETS_STILES
            }),
            'imange': forms.FileInput(attrs={
                'class': WIDGETS_STILES
            })
        }