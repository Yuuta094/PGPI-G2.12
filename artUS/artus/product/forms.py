from django import forms
from .models import Artwork

WIDGETS_STILES= 'w-full py-2 px-2 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model= Artwork
        fields= ('category','author','name','description','price', 'quantity', 'manufacturer','image' )
        
        
        widgets = {
            'category': forms.Select(attrs={
               'class': WIDGETS_STILES 
            }),
            'author': forms.TextInput(attrs={
                'class': WIDGETS_STILES
            }),
            'name': forms.TextInput(attrs={
                'class': WIDGETS_STILES
            }),
            'description': forms.Textarea(attrs={
                'class': WIDGETS_STILES
            }),
            'price': forms.TextInput(attrs={
                'class': WIDGETS_STILES
            }),
             'manufacturer': forms.TextInput(attrs={
                'class': WIDGETS_STILES
            }),
            'image': forms.FileInput(attrs={
                'class': WIDGETS_STILES
            })
        }