from django.db import models

class Citizen(models.Model):
    rm = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    voted = models.BooleanField(default=False)

class Candidate(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos')

class FirstTurn(models.Model):
    id = models.IntegerField(primary_key=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE)

class SecondTurn(models.Model):
    id = models.IntegerField(primary_key=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE)