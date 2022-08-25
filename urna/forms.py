from django import forms
from urna.models import Citizen

class loginForm(forms.Form):
    rm = forms.CharField(max_length=10, label='Registro de Matrícula')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label='Senha')

class register(forms.Form):
    name = forms.CharField(max_length=50, label='Nome')
    rm = forms.CharField(max_length=10, label='Registro de matrícula')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label='Senha')
    class meta:
        model = Citizen()
        fields = ['name', 'rm' , 'password']
    
    