from django.db import models

# Banco modelado por Richard

class Citizen(models.Model):
    rm = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    voted = models.BooleanField(default=False)

class Candidate(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    party = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    description = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos')
    is_ndTurn = models.BooleanField(default=False)
    getWinner = models.BooleanField(default=False)


class stTurn(models.Model):
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    citizen_id = models.ForeignKey(Citizen, on_delete=models.CASCADE)

class ndTurn(models.Model):
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    citizen_id = models.ForeignKey(Citizen, on_delete=models.CASCADE)
