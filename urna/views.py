from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from urna.forms import register, loginForm
from urna.models import Citizen, Candidate
import json

def login_view_GET(request, err):
    form = loginForm()
    return render(request, 'login.html', {'form': form})

def login_view_POST(request):
    form = loginForm(request.POST)
    if form.is_valid():
        form_rm = form.cleaned_data['rm']
        form_password = form.cleaned_data['password']

        user = Citizen.objects.filter(rm=form_rm, password=form_password)
        if user:
            if user[0].voted == False:
                request.session['logged_in_status'] = True
                return HttpResponseRedirect('../../')
            else:
                return HttpResponseRedirect('../../login/2')

    return HttpResponseRedirect('../../login/1')

def register_view_GET(request, err):
    form = register()
    return render(request, 'registrar.html', {'form': form})

def register_view_POST(request):
    form = register(request.POST)
    if form.is_valid():
        form_name = form.cleaned_data['name']
        form_rm = form.cleaned_data['rm']
        form_password = form.cleaned_data['password']

        new_user = Citizen(name=form_name, rm=form_rm, password=form_password)
        new_user.save()

        return HttpResponseRedirect('../../login/0')
    return HttpResponseRedirect('../../register/1')

def vote_view_GET(request):
    cand = Candidate.objects.filter()
    if request.session.get('logged_in_status'):
        return render(request, 'vote.html')
    else:
        return HttpResponseRedirect('../../login/0')

def vote_view_GET_candidates(request):
    form_id = request.GET.get('id')

    QueryCand = Candidate.objects.filter(id=form_id)
    if QueryCand:
        cand = {
            'name': QueryCand[0].name,
            'photo': QueryCand[0].photo,
            'party': QueryCand[0].party,
            'description': QueryCand[0].description,
        }
        return HttpResponse(cand)
    else:
        return HttpResponse(json.dump({'error': 'error'}), status=400, content_type='application/json')