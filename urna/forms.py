from django import forms
from urna.models import Citizen

class loginForm(forms.Form):
    name = forms.CharField(max_length=50, label='Nome')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label='Senha')


class register(forms.Form):
    name = forms.CharField(max_length=50, label='Nome')
    lastname = forms.CharField(max_length=50,  label='Sobrenome')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label='Senha')
    class meta:
        model = Citizen()
        fields = ['name', 'lastname', 'password']
    
    