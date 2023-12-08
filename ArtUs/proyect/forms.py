from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import *


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'w-full py-4 px-6 rounded-xl'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'w-full py-4 px-6 rounded-xl'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)
    

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid email/password.")
        if not user.check_password(password):
            raise forms.ValidationError("Invalid email/password.")
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.")
        
        # Set user_cache after successful authentication
        self.user_cache = user

        return self.cleaned_data

    def get_user(self):
        return self.user_cache 
    
    
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario','class': 'w-full py-4 px-6 rounded-xl'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Tu email','class': 'w-full py-4 px-6 rounded-xl'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Tu contraseña','class': 'w-full py-4 px-6 rounded-xl'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repite contraseña','class': 'w-full py-4 px-6 rounded-xl'}))
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ('id','username','email','password')
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario','class': 'w-full py-4 px-6 rounded-xl'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Tu email','class': 'w-full py-4 px-6 rounded-xl'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Tu contraseña','class': 'w-full py-4 px-6 rounded-xl'}))
 
class EditForm(PasswordChangeForm):
    pass


#                     #
#---- Nueeva obra ----#
#                     #

WIDGETS_STILES= 'w-full py-6 px-2 border-2 border-black rounded-lg'

class NewItemForm(forms.ModelForm):
    class Meta:
        model= Artwork
        fields= ('category','author','name','description','price', 'quantity', 'manufacturer','image' )
        labels = {
            'category': 'Categoría',
            'author': 'Autor',
            'name': 'Nombre',
            'description': 'Descripción',
            'price': 'Precio',
            'quantity': 'Cantidad',
            'manufacturer': 'Fabricante',
            'iamge': 'Imagen',
        }
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
            'price': forms.NumberInput(attrs={
                'class': WIDGETS_STILES,
                'min':0,
            }),
            'quantity': forms.NumberInput(attrs={
                'class': WIDGETS_STILES,
                'min':0,
            }),
             'manufacturer': forms.TextInput(attrs={
                'class': WIDGETS_STILES
            }),
            'image': forms.FileInput(attrs={
                'class': WIDGETS_STILES
            })
        }




class EditItemForm(forms.ModelForm):
    class Meta:
        model= Artwork
        fields= ('category','author','name','description','price', 'quantity', 'manufacturer','image' )
        labels = {
            'category': 'Categoría',
            'author': 'Autor',
            'name': 'Nombre',
            'description': 'Descripción',
            'price': 'Precio',
            'quantity': 'Cantidad',
            'manufacturer': 'Fabricante',
            'iamge': 'Imagen',
        }
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
            'price': forms.NumberInput(attrs={
                'class': WIDGETS_STILES
            }),
             'quantity': forms.NumberInput(attrs={
                'class': WIDGETS_STILES
            }),
             'manufacturer': forms.TextInput(attrs={
                'class': WIDGETS_STILES
            }),
            'image': forms.FileInput(attrs={
                'class': WIDGETS_STILES
            })
        }



#                #
#---- Compra ----#
#                #


WIDGETS_STILES= 'w-full py-2 px-2 rounded-xl border'

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['address', 'country', 'city', 'zip_code', 'telephone']
        labels = {
            'address': 'Dirección',
            'country': 'País',
            'city': 'Ciudad',
            'zip_code': 'Código Postal',
            'telephone': 'Teléfono',
        }
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
        
class PurchaseNotLoggedForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'address', 'country', 'city', 'zip_code', 'telephone']
        labels = {
            'customer': 'Correo electrónico',
            'address': 'Dirección',
            'country': 'País',
            'city': 'Ciudad',
            'zip_code': 'Código Postal',
            'telephone': 'Teléfono',
        }
        widgets = {
            'customer': forms.EmailInput(attrs={
            'class': WIDGETS_STILES
        }),
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
    
class EditOrderStateForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('ordernum', 'customer', 'total_price', 'address', 'country', 'city', 'zip_code', 'telephone')
        labels = {
            'status': 'Estado',
        }

        widgets = {
            'status': forms.Select(attrs={
                'class': 'WIDGETS_STILES' 
            }),
        }