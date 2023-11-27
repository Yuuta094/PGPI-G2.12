from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario','class': 'w-full py-4 px-6 rounded-xl'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Tu contraseña','class': 'w-full py-4 px-6 rounded-xl'}))

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
 