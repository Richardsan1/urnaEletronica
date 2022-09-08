from django import forms
from urna.models import Citizen, Turns

class loginForm(forms.Form):
    rm = forms.CharField(max_length=10, label='Registro de Matrícula')

class register(forms.Form):
    name = forms.CharField(max_length=50, label='Nome')
    rm = forms.CharField(max_length=10, label='Registro de matrícula')
    class meta:
        model = Citizen()
        fields = ['name', 'rm']
    
class vote (forms.Form):
    candidate = forms.IntegerField(label='ID do candidato')
    citizen = forms.IntegerField(label='ID do cidadão')
    second_turn = forms.BooleanField(label='Segundo turno')
    class meta:
        model = Turns()
        fields = ['candidate_id', 'citizen_id', 'second_turn']