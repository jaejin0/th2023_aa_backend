from django.db import models

# Create your models here.
class Member(models.Model):
    flightNumber = models.CharField(max_length=4)
    date = models.CharField(max_length=10)
    checkInTime = models.CharField(max_length=15)
    tsa = models.CharField(max_length=15)
    walkingTime = models.CharField(max_length=15)