from django.db import models
import requests

# Create your models here.
class Beneficiary(models.Model):
    phone_num = models.CharField(primary_key=True, max_length=12)
    #name = models.CharField(max_length=100)
    food = models.BooleanField(default=False)
    diapers = models.BooleanField(default=False)
    sanitary = models.BooleanField(default=False)
    blankets = models.BooleanField(default=False)

    def __str__(self):
        return str(self.phone_num)

class Location(models.Model):
    longitude = models.FloatField()
    laditude = models.FloatField()

    def Location(self, road1, road2):
        coords = requests.get('https://www.google.com/maps/place/'+road1+' & '+road2)
        coords.findall(r'll=(.*?)" item', coords.text)[0].split(',')
        self.laditude = coords[0]
        self.laditude = coords[1]