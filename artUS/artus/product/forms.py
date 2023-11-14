from django import forms
from .models import Artwork

WIDGETS_STILES= 'w-full py-4 px-6 rounded-xl border'

class EdititemForm(forms.ModelForm):
    class Meta:
        model= Artwork
        fields= ('name','description','price', 'image')
        
        widgets = {
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