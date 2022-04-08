from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.forms import CharField
import requests
from datetime import datetime

# Create your models here.
class Beneficiary(models.Model):
    phone_num = models.CharField(primary_key=True, max_length=12)
    #name = models.CharField(max_length=100)
    food = models.BooleanField(default=False)
    diapers = models.BooleanField(default=False)
    sanitary = models.BooleanField(default=False)
    blankets = models.BooleanField(default=False)
    longitude = models.FloatField(null=True, default=0.0)
    latitude = models.FloatField(null=True, default=0.0)
    language = models.CharField(default="english", max_length=15)

    def __str__(self):
        return str(self.phone_num)



class Organization(models.Model):
    organization_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    address_one = models.CharField(max_length=100)
    address_two = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=5)
    food = models.BooleanField(default=False)
    diapers = models.BooleanField(default=False)
    sanitary = models.BooleanField(default=False)
    blankets = models.BooleanField(default=False)
    stayable = models.BooleanField(default=False)

    def __str__(self):
        return str(self.organization_name)

class Event(models.Model):
    organization_name = models.CharField(max_length=100)
    organizer_firstname = models.CharField(max_length=100, null=True)
    organizer_lastname = models.CharField(max_length=100, null=True)
    email=models.EmailField(null=True)
    event_name = models.CharField(max_length=100)
    event_description = models.CharField(max_length=100)
    start_datetime = models.DateTimeField(default=datetime.now, blank=True)
    end_datetime = models.DateTimeField(default=datetime.now, blank=True)
    address_one = models.CharField(max_length=100)
    address_two = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=5)
    food = models.BooleanField(default=False)
    diapers = models.BooleanField(default=False)
    sanitary = models.BooleanField(default=False)
    blankets = models.BooleanField(default=False)
    def __str__(self):
        return str(self.event_name + ' by ' + self.organization_name)
