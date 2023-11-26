from django import forms
from .models import Artwork

WIDGETS_STYLES= 'w-full py-2 px-2 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model= Artwork
        fields= ('author','name','description','price', 'quantity', 'manufacturer','image' )
        
        
        widgets = {
            
            'author': forms.TextInput(attrs={
                'class': WIDGETS_STYLES
            }),
            'name': forms.TextInput(attrs={
                'class': WIDGETS_STYLES
            }),
            'description': forms.Textarea(attrs={
                'class': WIDGETS_STYLES
            }),
            'price': forms.TextInput(attrs={
                'class': WIDGETS_STYLES
            }),
             'manufacturer': forms.TextInput(attrs={
                'class': WIDGETS_STYLES
            }),
            'image': forms.FileInput(attrs={
                'class': WIDGETS_STYLES
            })
        }




class EditItemForm(forms.ModelForm):
    class Meta:
        model= Artwork
        fields= ('category','author','name','description','price', 'quantity', 'manufacturer','image' )
        
        
        widgets = {
            'category': forms.Select(attrs={
               'class': WIDGETS_STYLES 
            }),
            'author': forms.TextInput(attrs={
                'class': WIDGETS_STYLES
            }),
            'name': forms.TextInput(attrs={
                'class': WIDGETS_STYLES
            }),
            'description': forms.Textarea(attrs={
                'class': WIDGETS_STYLES
            }),
            'price': forms.TextInput(attrs={
                'class': WIDGETS_STYLES
            }),
             'manufacturer': forms.TextInput(attrs={
                'class': WIDGETS_STYLES
            }),
            'image': forms.FileInput(attrs={
                'class': WIDGETS_STYLES
            })
        }