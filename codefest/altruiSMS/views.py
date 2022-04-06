from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import Beneficiary
import re 
from django.forms.models import model_to_dict
from django.db.models import CharField
from django.db.models import  Q
import datetime
import calendar
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import requests

@api_view(["GET", "POST"])
@csrf_exempt
# @permission_classes([IsAuthenticated])
def sms(request):
    output = request.body.decode("utf-8")
    payload = dict([x.split('=') for x in output.split('&')])
    food = payload.get('Body', '').lower()
    to_number = payload.get('From')
    url = "https://www.themealdb.com/api/json/v1/1/search.php?s=" + food

    response = requests.request("GET", url).json()


    # resp = MessagingResponse()
    # msg = resp.message()

    r = ""
    r += "\n Ingredients: \n"

    for x in response["meals"][0]:
        if ("strIngredient" in x):
            if (response['meals'][0][x] != "" and response['meals'][0][x] != None):
                r += response["meals"][0][x] + "\n"

    r += "Recipe: \n"
    r += response['meals'][0]['strInstructions']
    # msg.body(r)

    client = Client("", "")

    message = client.messages \
        .create(
            body=r,
            from_='+15854407446',
            to= to_number
        )

    print(message.sid)
    return message.sid
