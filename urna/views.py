from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from urna.forms import register, loginForm



def login_view_GET(request, err):
    form = loginForm()
    return render(request, 'login.html', {'form': form})

def login_view_POST(request):
    form = loginForm(request.POST)
    if form.is_valid():    
        return HttpResponseRedirect('../../')

    return HttpResponseRedirect('../../login/1')

def register_view_GET(request, err):
    form = register()
    return render(request, 'registrar.html', {'form': form})

def register_view_POST(request):
    form = register(request.POST)
    if form.is_valid():
        form_name = form.cleaned_data['name']
        form_lastname = form.cleaned_data['lastname']
        form_password = form.cleaned_data['password']

        new_user = Votante(name=form_name, lastname=form_lastname, password=form_password)
        new_user.save()

        return HttpResponseRedirect('../../login/0')
    return HttpResponseRedirect('../../register/1')

def vote_view(request):
    if True:
        return render(request, 'vote.html')
