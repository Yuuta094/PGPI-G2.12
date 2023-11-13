from django import forms
from .models import Obra

WIDGETS_STILES= 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model= Obra
        fields= ('category','name','description','price', 'image')
        
        widgets = {
            'categroy': forms.Select(attrs={
               'class': WIDGETS_STILES 
            }),
            'name': forms.Textarea(attrs={
                'class': WIDGETS_STILES
            }),
            'description': forms.Textarea(attrs={
                'class': WIDGETS_STILES
            }),
            'price': forms.TextInput(attrs={
                'class': WIDGETS_STILES
            }),
            'image': forms.FileInput(attrs={
                'class': WIDGETS_STILES
            })
        }