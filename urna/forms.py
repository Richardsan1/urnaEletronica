from django import forms
from urna.models import Citizen
# richard modelou os forms
class loginForm(forms.Form):
    rm = forms.CharField(max_length=10, label='Registro de Matrícula')

class register(forms.Form):
    name = forms.CharField(max_length=50, label='Nome')
    rm = forms.CharField(max_length=10, label='Registro de matrícula')
    class meta:
        model = Citizen()
        fields = ['name', 'rm']