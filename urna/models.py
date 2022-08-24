from django.db import models

class Citizen(models.Model):
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    
class Candidato(models.Model):
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/persons')
    votes = models.IntegerField(default=0)
    second_votes = models.IntegerField(default=0)
    secondTurn = models.BooleanField(default=False)