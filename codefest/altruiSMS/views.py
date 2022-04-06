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
    incoming = payload.get('Body', '').lower()[:-1]
    to_number = "+" + payload.get('From')[3:]

    url = "https://www.themealdb.com/api/json/v1/1/search.php?s=" + incoming

    response = requests.request("GET", url).json()

    #making a beneficiary
    person = Beneficiary(phone_num = to_number)
    person.save()


    r = ""
    #adding to and removing from the data base
    items = ["food", "diaper", "blanket", "sanitary"]
    removed = []
    added = []
    if new(to_number):
        r = "Hi! I’m chatbot, I am here to help you get access to the resources you need. By responding to this text you can opt into receiving notifications as local organizations are holding drives, or giving away specific items. The items you can choose to be notified about are food, diapers, blankets, and sanitary items. Reply to this text with the names of the items you wish to be notified about in the future."
    else:
        if incoming == "help":
            r = help_menu()
        if "food" in items:
            if "remove food" in items:
                removed.append("food")
                person.food = False
            else:
                added.append("food")
                person.food = True
        if "diaper" in items:
            if "remove diaper" in items:
                removed.append("diapers")
                person.diapers = False
            else:
                added.append("diapers")
                person.diapers = True
        if "blanket" in items:
            if "remove blanket" in items:
                removed.append("blankets")
                person.blankets = False
            else:
                added.append("blankets")
                person.blankets = True
        if "sanitary" in items:
            if "remove sanitary" in items:
                removed.append("sanitary items")
                person.sanitary = False
            else:
                added.append("sanitary items")
                person.sanitary = True

        if len(added) > 0:
            r += "Sounds good! To make sure we are notifying you about distributions of "+list_to_string(added)+" in your area please reply to this text with either the word “zip” followed by a zip code near you or the word “intersection” followed by names of two intersecting streets near you\n"

        if len(removed) > 0:
            r += "Sounds good, I will no longer notify you about avalible " + list_to_string(removed) + "\n"


        if "shelter" in incoming:
            if person.location == None:
                r = 'To find a shelter for you I need some idea of your location first. Send a message saying "zip" followed by the zip code you are in, or "intersection" and the name of two streets that intersect near you. After doing this, text shelter again, and I can find the one closest to you'
            else:
                pass

        #adding location data
        if "zip" in incoming:
            #set person.location to int(item[5:])
            pass
        elif "intersection" in incoming:
            if len(incoming.split()) == 3:
                road1, road2 = incoming.split()[1], incoming.split()[2]

            elif len(incoming.split()) == 5:
                road1 = incoming.split()[1].append(" "+incoming.split()[2])
                road2 = incoming.split()[3].append(" "+incoming.split()[4])
            if intersect_valid(road1, road2):
                #set person location
                r += "Thanks!! You will now be notified when there is a distribution near you."
            else:
                r += 'Hm, I could not find that intersection, could you try entering another one (make sure to include the word "intersection" before the street names)'

        if r == "":
            r = "I'm sorry, I'm not sure what that means, for a full list of things I can do text \"help\""

    client = Client("AC86f5c09c4f505b9a005468ffcf760039", "3c47e7ec29619f8f27c6a11115a5d433")

    message = client.messages \
        .create(
        body=r,
        from_='+18126055840',  # sams: '+15854407446',
        to=to_number
    )

    print(message.sid)
    return HttpResponse('')


#returns true if num not in which phone list
def new(num, which="master"):
    if Beneficiary.objects.exists():
        return False
    else:
        return True

#returns true if found intersection
def intersect_valid(road1, road2):
    return True

def list_to_string(lst):
    s = ""
    if len(lst) > 0:
        s = lst[0]
        lst = lst[1:]
    if len(lst) > 1:
        while len(lst) != 0:
            if len(lst) == 1:
                s += ", and "+lst[0]
                lst = lst[1:]
            else:
                s += ", "+lst[0]
                lst = lst[1:]


def help_menu():
    s = "-To change what items you are notified about you can just ask me to “remove” or “add” followed by an item name\n"
    s += '-To get a list of items that I can notify you about, you can just text "items"\n'
    s += '-To change your location, text “change location to” followed by the new zip code or intersection (names of two streets)\n'
    s += '-To find the nearest shelter to you, text “shelter” followed by a zip code or intersection you are looking for a shelter near. If you have already given us a location, you can just text “shelter”\n'
    return s