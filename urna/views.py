from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from urna.forms import register, loginForm
from django.db.models import Q
from urna.models import Citizen, Candidate, stTurn, ndTurn
import json

# estruturação do site feita por Richard

# login page
def login_GET(request, err):
    form = loginForm()
    return render(request, 'login.html', {'form': form})

# log
def login_POST(request):
    form = loginForm(request.POST)
    if form.is_valid():
        form_rm = form.cleaned_data['rm']

        user = Citizen.objects.filter(rm=form_rm)
        if user:
            if user[0].voted == False:
                request.session['logged_in_status'] = True
                request.session['logged_in_user'] = user[0].rm

                votos = stTurn.objects.all().count()
                pessoas = Citizen.objects.all().filter().count()
                if votos == pessoas:
                    request.session['turn'] = 2
                else:
                    request.session['turn'] = 1

                print(request.session['turn'])
                return HttpResponseRedirect('../../')
            else:
                return HttpResponseRedirect('../../login/2')

    return HttpResponseRedirect('../../login/1')

# register page
def register_GET(request, err):
    form = register()
    return render(request, 'registrar.html', {'form': form})

# put data on database
def register_POST(request):
    form = register(request.POST)
    if form.is_valid():
        form_name = form.cleaned_data['name']
        form_rm = form.cleaned_data['rm']

        if Citizen.objects.filter(rm=form_rm):
            return HttpResponseRedirect('../2')
        new_user = Citizen(name=form_name, rm=form_rm)
        new_user.save()

        return HttpResponseRedirect('../../login/0')
    return HttpResponseRedirect('../../register/1')

# index
def vote_GET(request):
    if request.session.get('logged_in_status'):
        if Citizen.objects.filter(rm=request.session['logged_in_user'])[0].voted:
            request.session['logged_in_status'] = False
            return HttpResponseRedirect('../login/2')
        else:
            return render(request, 'vote.html')
    else:
        return HttpResponseRedirect('candidatos/')

# vote
def vote_POST(request):
    if request.session['logged_in_status']:
        form = request.POST
        
        form_candidate_id = form['vote']
        current_user = request.session['logged_in_user']

        cand = Candidate.objects.get(id=form_candidate_id)
        user = Citizen.objects.get(rm=current_user)

        if request.session['turn'] == 1:
            vote = stTurn(citizen_id=user, candidate_id=cand)
        else:
            if cand.is_ndTurn:
                vote = ndTurn(citizen_id=user, candidate_id=cand)
            else: 
                return HttpResponseRedirect('../')

        vote.save()
        user.voted = True
        user.save()

        return render(request, "confirm.html", {'candidateName': cand.name})

    else:
        return HttpResponseRedirect('../')

# API
def vote_GET_candidates(request):
    if request.GET.get('id'):
        form_id = request.GET.get('id')
        if request.session['turn'] == 1:
            QueryCand = Candidate.objects.filter(id=form_id)
        else: 
            QueryCand = Candidate.objects.filter(id=form_id, is_ndTurn=True)
        
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

#logout
def logout_GET(request):
    request.session['logged_in_status'] = False
    request.session['logged_in_user'] = ""
    
    votos = stTurn.objects.all().count()
    votos2 = ndTurn.objects.all().count()
    pessoas = Citizen.objects.all()

    if votos == pessoas.count() and request.session['turn'] == 1:
        pessoas.update(voted=False)
        request.session['turn'] = 2

        primeiroTurn = stTurn.objects.all().filter(~Q(candidate_id=0))
        candidates = Candidate.objects.all().filter(~Q(id=0))
        i = 0
        venc = False
        while i < candidates.count():
            if primeiroTurn.filter(candidate_id=candidates[i]).count() > primeiroTurn.count()//2:   
                cand = Candidate.objects.get(id=candidates[i].id)
                cand.getWinner = True
                cand.save()
                break
            i += 1
        else:
            venc = True
        
        if venc:
            candidatesVotes = []
            for candidate in candidates:
                candidatesVotes.append({candidate.id : primeiroTurn.filter(candidate_id=candidate.id).count()})
            candidatesVotes.sort(key=lambda x: list(x.values())[0], reverse=True)
            print(candidatesVotes)
            
            if list(candidatesVotes[0].values())[0] >= list(candidatesVotes[1].values())[0]:
                if list(candidatesVotes[0].values())[0] >= list(candidatesVotes[2].values())[0]:
                    cand = Candidate.objects.get(id=list(candidatesVotes[0].keys())[0])
                    cand.is_ndTurn = True
                    cand.save()
                    if list(candidatesVotes[1].values())[0] >= list(candidatesVotes[2].values())[0]:
                        cand = Candidate.objects.get(id=list(candidatesVotes[1].keys())[0])
                        cand.is_ndTurn = True
                        cand.save()
                    else:
                        cand = Candidate.objects.get(id=list(candidatesVotes[2].keys())[0])
                        cand.is_ndTurn = True
                        cand.save()
                else:
                    cand = Candidate.objects.get(id=list(candidatesVotes[2].keys())[0])
                    cand.is_ndTurn = True
                    cand.save()
            else:
                cand = Candidate.objects.get(id=list(candidatesVotes[1].keys())[0])
                cand.is_ndTurn = True
                cand.save()
                if list(candidatesVotes[0].values())[0] >= list(candidatesVotes[2].values())[0]:
                    cand = Candidate.objects.get(id=list(candidatesVotes[0].keys())[0])
                    cand.is_ndTurn = True
                    cand.save()
                else:
                    cand = Candidate.objects.get(id=list(candidatesVotes[2].keys())[0])
                    cand.is_ndTurn = True
                    cand.save()

    elif votos2 == pessoas.count() and request.session['turn'] == 2:
        segundoTurn = ndTurn.objects.all().filter(~Q(candidate_id=0))
        candidates = Candidate.objects.all().filter(is_ndTurn=True)
        i = 0
        while i < candidates.count():
            if segundoTurn.filter(candidate_id=candidates[i]).count() > segundoTurn.count()//2:   
                cand = Candidate.objects.get(id=candidates[i].id)
                cand.getWinner = True
                cand.save()
                break
            i += 1
        else:
            if segundoTurn.filter(candidate_id=candidates[0]).count() == segundoTurn.filter(candidate_id=candidates[1]).count():
                
                if candidates[0].age > candidates[1].age:
                    cand = Candidate.objects.get(id=candidates[0].id)
                else: 
                    cand = Candidate.objects.get(id=candidates[1].id)
                cand.getWinner = True
                cand.save()
        
    return HttpResponseRedirect('../candidatos')

def view_candidates_GET(request):
    if Candidate.objects.all().filter(getWinner=True):
        return render(request, 'candidatos.html', {'candidatos': Candidate.objects.all().filter(getWinner=True), 'turn': 'Vencedor das eleições', 'notEnded': False})

    candidatos = Candidate.objects.all().filter(is_ndTurn=True)
    if candidatos:
        turno = "Segundo turno"
    else: 
        candidatos = Candidate.objects.all().filter(~Q(id=0))
        turno = "Primeiro turno" 
    return render(request, 'candidatos.html', {'candidatos': candidatos, 'turn': turno, 'notEnded': True})

def teste(request):
    candidato = Candidate.objects.all().filter(~Q(id=0))
    candidato = list(candidato)
    return HttpResponse(candidato)
    # return render(request, 'confirm.html')