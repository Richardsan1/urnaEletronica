from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from urna.forms import register, loginForm, vote
from urna.models import Citizen, Candidate
import json

# estruturação do site feita por Richard

# login page
def login_view_GET(request, err):
    form = loginForm()
    return render(request, 'login.html', {'form': form})

# log
def login_view_POST(request):
    form = loginForm(request.POST)
    if form.is_valid():
        form_rm = form.cleaned_data['rm']

        user = Citizen.objects.filter(rm=form_rm)
        if user:
            if user[0].voted == False:
                request.session['logged_in_status'] = True
                return HttpResponseRedirect('../../')
            else:
                return HttpResponseRedirect('../../login/2')

    return HttpResponseRedirect('../../login/1')

# register page
def register_view_GET(request, err):
    form = register()
    return render(request, 'registrar.html', {'form': form})

# put data on database
def register_view_POST(request):
    form = register(request.POST)
    if form.is_valid():
        form_name = form.cleaned_data['name']
        form_rm = form.cleaned_data['rm']

        new_user = Citizen(name=form_name, rm=form_rm)
        new_user.save()

        return HttpResponseRedirect('../../login/0')
    return HttpResponseRedirect('../../register/1')

# index
def vote_view_GET(request):
    if request.session.get('logged_in_status'):
        form = vote()
        return render(request, 'vote.html', {'form': form})
    else:
        return HttpResponseRedirect('../../login/0')

# API
def vote_view_GET_candidates(request):
    if request.GET.get('id'):
        form_id = request.GET.get('id')
        QueryCand = Candidate.objects.filter(id=form_id)
        
        if QueryCand:
            cand = {
                'name': QueryCand[0].name,
                'photo': str(QueryCand[0].photo),
                'party': QueryCand[0].party,
                'description': QueryCand[0].description,
            }
            return HttpResponse(json.dumps(cand, indent=4), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'error': 'error'}, indent=4), status=400, content_type='application/json')
    else:
        return HttpResponse(json.dumps({'error': 'error'}, indent=4), status=400, content_type='application/json')

# logout and terminate vote
def logout_view_GET(request):
    request.session['logged_in_status'] = False
    return HttpResponseRedirect('../../')

# vote
def vote_view_POST(request):
    if request.session['logged_in_status']:
        request.session['logged_in_status'] = False
        form = request.POST
        print(form)
    return HttpResponseRedirect('../')
