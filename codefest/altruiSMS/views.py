from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import Beneficiary, Organization, Event
import re 
from django.forms.models import model_to_dict
from django.db.models import CharField
from django.db.models import  Q
import datetime
import calendar
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import requests
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import translators as ts

@api_view(["GET", "POST"])
@csrf_exempt
# @permission_classes([IsAuthenticated])
def sms(request):
    output = request.body.decode("utf-8")
    payload = dict([x.split('=') for x in output.split('&')])
    incoming_og = payload.get('Body', '').lower()
    to_number = "+" + payload.get('From')[3:]

    url = "https://www.themealdb.com/api/json/v1/1/search.php?s=" + incoming_og

    response = requests.request("GET", url).json()

    #converting incoming to no special chars
    incoming = ''
    for c in incoming_og:
        if c.isalpha():
            incoming += c
        elif c == "+":
            incoming += ' '

    r = ""
    road_words = ['rd','road','st','street','ave','avenue','wy','way','cir','circle','ct','court','expy','expressway','fwy','freeway','ln','lane','pky','parkway','square','sq','tpk','turnpike']
    lang_dict = {'english':'en','spanish':'es','french':'fr','chinese':'zh','arabic':'ar','russian':'ru','german':'de','italian':'it','japanese':'jp','korean':'ko'}
    #adding to and removing from the data base
    items = ["food", "diaper", "blanket", "sanitary"]
    removed = []
    added = []
    print(incoming)
    if new(to_number):
        r = "Hi! I’m Phil, AlturiSMS' chatbot, I am here to help you get access to the resources you need. By responding to this text you can opt into receiving notifications as local organizations are holding drives, or giving away specific items. The items you can choose to be notified about are food, diapers, blankets, and sanitary items. Reply to this text with the names of the items you wish to be notified about in the future. (para mensajes en espanol, texto \"espanol\")" #(for a different language type \"language\")"
        person = Beneficiary.objects.create(phone_num=to_number)
        person.save()
    else:
        person = Beneficiary.objects.get(phone_num=to_number)
        if person.language != 'en':
            incoming = ts.google(incoming, to_language='en')
        if "help me" in incoming:
            r = help_menu()
        if "hi" == incoming or "hey" == incoming or "hello" == incoming:
            r = "Hi! I’m Phil, AlturiSMS' chatbot, I am here to help you get access to the resources you need. By responding to this text you can opt into receiving notifications as local organizations are holding drives, or giving away specific items. The items you can choose to be notified about are food, diapers, blankets, and sanitary items. Reply to this text with the names of the items you wish to be notified about in the future. (para mensajes en espanol, texto \"espanol\")"  # (for a different language type \"language\")"
        if "thank you" == incoming:
            r = "Youre welcome!"
        if "items" in incoming:
            r += "Here are the items you can opt into (you can do so by replying with the names of the items you would like to be notified about):\n"+items[0]
            for item in items[1:]:
                r += ", "+item
        # if "language" in incoming:
        #     r += "what language? english, spanish, french, chinese, arabic, russian, german, italian, japanese, or korean"
        # for lang in lang_dict.keys():
        #     if lang in incoming and lang != "english":
        #         person.language = lang_dict[lang]
        #         r = "Hi!  I’m chatbot, I am here to help you get access to the resources you need. By responding to this text you can opt into receiving notifications as local organizations are holding drives, or giving away specific items. The items you can choose to be notified about are food, diapers, blankets, and sanitary items. Reply to this text with the names of the items you wish to be notified about in the future."

        if "espanol" in incoming:
            person.language = "es"
            r = "Hi!  I’m Phil, UlturiSMS' chatbot, I am here to help you get access to the resources you need. By responding to this text you can opt into receiving notifications as local organizations are holding drives, or giving away specific items. The items you can choose to be notified about are food, diapers, blankets, and sanitary items. Reply to this text with the names of the items you wish to be notified about in the future."
        if "english" in incoming:
            person.language = "en"
            r = "Hi!  I’m phil AlturiSMS' chatbot, I am here to help you get access to the resources you need. By responding to this text you can opt into receiving notifications as local organizations are holding drives, or giving away specific items. The items you can choose to be notified about are food, diapers, blankets, and sanitary items. Reply to this text with the names of the items you wish to be notified about in the future."
        if "food" in incoming:
            if "remove food" in items:
                removed.append("food")
                person.food = False
            else:
                added.append("food")
                person.food = True
        if "diaper" in incoming:
            if "remove diaper" in items:
                removed.append("diapers")
                person.diapers = False
            else:
                added.append("diapers")
                person.diapers = True
        if "blanket" in incoming:
            if "remove blanket" in items:
                removed.append("blankets")
                person.blankets = False
            else:
                added.append("blankets")
                person.blankets = True
        if "sanitary" in incoming:
            if "remove sanitary" in items:
                removed.append("sanitary items")
                person.sanitary = False
            else:
                added.append("sanitary items")
                person.sanitary = True

        if len(added) > 0:
            s = list_to_string(added)
            r = "Sounds good! To make sure we are notifying you about distributions of "+s+" in your area please reply to this text with either the word “intersection” followed by names of two intersecting streets near you\n"

        if len(removed) > 0:
            s = list_to_string(removed)
            r = "Sounds good, I will no longer notify you about avalible " +s+ "\n"

        if ("remove" or "delete") and ("location" or "intersection") in incoming:
            person.latitude = 0.0
            person.longitude = 0.0
            r += "Your location has been deleted"

        # if "address" in incoming:
        #     print("here")
        #     coords = (address_to_ll("12417 Borges Ave","MD"))
        #     r += "Coords: ["+str(coords[0])+','+str(coords[1])+']'

        # if "directions" in incoming:
        #     if "walking" in incoming:
        #         r += get_directions(str(person.latitude), str(person.longitude), "40.00890629403572","-75.29311694445455", mode="walking")
        #     else:
        #         r += get_directions(str(person.latitude), str(person.longitude), "40.00890629403572","-75.29311694445455")

        if "shelter" in incoming:
            if person.longitude == person.latitude == 0.0:
                r = 'To find a shelter for you I need some idea of your location first. Send a message saying "intersection" and the name of two streets that intersect near you. After doing this, text shelter again, and I can find the one closest to you'
            else:
                closest = find_shelter(person.latitude,person.longitude)
                address = closest.address_one+', '+closest.address_two+', '+closest.city+' '+closest.zipcode
                if "directions to shelter" in incoming:
                    coords = address_to_ll(closest)
                    if "walk" in incoming:
                        r += "Here are your directions: \n" + get_directions(person.latitude, person.longitude,coords[0], coords[1],mode="walking")
                    else:
                        r += "Here are your directions: \n"+get_directions(person.latitude, person.longitude,coords[0],coords[1])
                else:
                    r += 'The shelter closest to you is '+closest.organization_name+' Here is the address: '+address+' For directions to this shelter just text me "directions to shelter."\n Make sure we have your most recent location in order to provide you with the actual nearest shelter. If your not sure how to do this, text "help me" for an explanation.'

        elif "intersection" in incoming:
            found = False
            split = incoming.split()[1:]
            for word in split:
                if word in road_words and word != "and":
                    road1 = ' '.join(split[:split.index(word) + 1])
                    road2 = ' '.join(split[split.index(word) + 1:])
                    set_location(person, road1, road2)
                    r += "Got it! Thanks!.\n"
                    #r += "Coords: ["+str(person.latitude)+','+str(person.longitude)+']'
                    found = True
                    break
            if not found:
                r += 'Hm, I could not find that intersection, could you try entering another one (make sure to include the word "intersection" before the street names)'

        if r == "":
            r = "I'm sorry, I'm not sure what that means, for a full list of things I can do text \"help me\""

    person.save()

    if person.language != "en":
        r = ts.google(r,from_language='en',to_language=person.language)
    client = Client("AC86f5c09c4f505b9a005468ffcf760039", "3c47e7ec29619f8f27c6a11115a5d433")

    message = client.messages \
        .create(
        body=r,
        from_='+18126055840',  # sams: '+15854407446',
        to=to_number
    )

    print(message.sid)
    return HttpResponse('')


class Index(LoginRequiredMixin, View):
    template = 'index.html'
    login_url = '/login/'


    def get(self, request):
        today = datetime.datetime.today()
        my_upcoming_event = Event.objects.all().filter(organization_name=self.request.user, start_datetime__gte=today).order_by('start_datetime').first()
        upcoming_events = Event.objects.all().filter(start_datetime__gte=today).order_by('start_datetime')
        upcoming_events_list = []
        for event in upcoming_events:
            event_list = []
            event_list.append(event.event_name)
            event_list.append(' '.join([event.address_one, event.address_two, event.city, event.zipcode]))
            event_list.append(event.organization_name)
            event_list.append(event.start_datetime.strftime("%Y-%m-%d %H:%M"))
            event_list.append(event.end_datetime.strftime("%Y-%m-%d %H:%M"))
            event_list.append(event.email)
            upcoming_events_list.append(event_list)
        if my_upcoming_event is not None:
            upcoming_event_datetime = my_upcoming_event.start_datetime.strftime("%Y-%m-%d %H:%M")
            return render(request, self.template, {'username':self.request.user, 'upcoming_event_datetime':upcoming_event_datetime, 'upcoming_events':upcoming_events_list})
        else:
            return render(request, self.template, {'username':self.request.user, 'upcoming_events':upcoming_events_list})


class CreateEvent(LoginRequiredMixin, View):
    template = 'create_event.html'
    login_url = '/login/'

    def get(self, request):
        placeholder_datetime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        return render(request, self.template, {'username':self.request.user, 'placeholder_datetime': placeholder_datetime})

    def post(self, request):
        event = Event(organization_name=self.request.user, organizer_firstname=request.POST['first_name'] \
            , event_name=request.POST['event_name'], event_description=request.POST['event_description']
            , organizer_lastname=request.POST['last_name'], email=request.POST['email'],  \
                address_one=request.POST['address_one'], address_two=request.POST['address_two']\
                    ,start_datetime=request.POST['event-starttime'], end_datetime=request.POST['event-endtime'] \
                    , city=request.POST['city'], zipcode=request.POST['zipcode'], food=change_on_to_true(request.POST.get('food', False)), \
                        diapers=change_on_to_true(request.POST.get('diapers', False)), \
                            sanitary=change_on_to_true(request.POST.get('sanitary', False))\
                                , blankets=change_on_to_true(request.POST.get('blankets', False))\
                                    )
        event.save()

        client = Client("AC86f5c09c4f505b9a005468ffcf760039", "3c47e7ec29619f8f27c6a11115a5d433")
        if event.food == True:
            all_food = Beneficiary.objects.all().filter(food=True)
            for ben in all_food:
                message = client.messages \
                    .create(
                    body= "Event notification: \n"+str(event.organization_name)+" is having a food distribution event ( "+str(event.event_name)+" )from"+str(event.start_datetime)+' to '+str(event.end_datetime)+'. The address is: '+str(event.address_one)+" "+str(event.address_two)+" "+str(event.city)+" "+str(event.zipcode)+"\n Heres a description of the event: "+str(event.event_description),
                    from_='+18126055840',  # sams: '+15854407446',
                    to= ben.phone_num
                )
            print(message.sid)
        if event.diapers == True:
            all_diapers = Beneficiary.objects.all().filter(diapers=True)
            for ben in all_diapers:
                message = client.messages \
                    .create(
                    body="Event notification: \n" + str(event.organization_name) + " is having a diaper distribution event ( " + str(event.event_name) + " )from" + str(event.start_datetime) + ' to ' + str(event.end_datetime) + '. The address is: ' + str(event.address_one) + " " + str(event.address_two) + " " + (event.city) + " " + (event.zipcode)+"\n Heres a description of the event: "+str(event.event_description),
                    from_ = '+18126055840',  # sams: '+15854407446',
                    to = ben.phone_num
                )
                print(message.sid)
        if event.sanitary == True:
            all_sanitary = Beneficiary.objects.all().filter()(sanitary=True)
            for ben in all_sanitary:
                message = client.messages \
                    .create(
                    body="Event notification: \n" + str(event.organization_name) + " is having a diaper distribution event ( " + str(event.event_name) + " )from" + str(event.start_datetime) + ' to ' + str(event.end_datetime) + '. The address is: ' + str(event.address_one) + " " + str(event.address_two) + " " + (event.city) + " " + (event.zipcode)+"\n Heres a description of the event: "+str(event.event_description),
                    from_ = '+18126055840',
                    to = ben.phone_num
                )
                print(message.sid)
        if event.blankets == True:
            all_blankets = Beneficiary.objects.all().filter(blankets=True)
            for ben in all_blankets:
                message = client.messages \
                    .create(
                    body="Event notification: \n" + str(event.organization_name) + " is having a diaper distribution event ( " + str(event.event_name) + " )from" + str(event.start_datetime) + ' to ' + str(event.end_datetime) + '. The address is: ' + str(event.address_one) + " " + str(event.address_two) + " " + (event.city) + " " + (event.zipcode)+"\n Heres a description of the event: "+str(event.event_description),
                    from_ = '+18126055840',  # sams: '+15854407446',
                    to = ben.phone_num
                )
                print(message.sid)


        return HttpResponseRedirect('/')

class Register(View):
    template = 'register.html'

    def get(self, request):
        return render(request, self.template)
    
    def post(self, request):
        organization = Organization(organization_name=request.POST['organization_name'], first_name=request.POST['first_name'] \
            , last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'], \
                address_one=request.POST['address_one'], address_two=request.POST['address_two']\
                    , city=request.POST['city'], zipcode=request.POST['zipcode'], food=change_on_to_true(request.POST.get('food', False)), \
                        diapers=change_on_to_true(request.POST.get('diapers', False)), \
                            sanitary=change_on_to_true(request.POST.get('sanitary', False))\
                                , blankets=change_on_to_true(request.POST.get('blankets', False))\
                                    , stayable=change_on_to_true(request.POST.get('stayable')))
        organization.save()
        user = User.objects.create_user(username=request.POST['organization_name'], email=request.POST['email'], password=request.POST['password'], is_staff=False)
        user.save()
        return HttpResponseRedirect('/login')
    
    

class Logout(View):
    template = "login.html"

    def get(self, request):
        logout(request)
        return render(request, self.template)

class Login(View):
    template = 'login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template, {'form': form})


    def post(self, request):
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, self.template, {'form': form})

#returns true if num not in which phone list
def new(num):
    if Beneficiary.objects.filter(phone_num=num).exists():
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
    return s


def set_location(person, road1, road2):
    req = requests.get('https://www.google.com/maps/place/'+road1+' & '+road2)
    coords = re.search(r'\[null,null,[+-]?([0-9]+\.[0-9]{10,}),[+-]?([0-9]+\.[0-9]+|\.[0-9]+)]', req.text) #[0].split(',')
    if coords is not None:
        person.latitude = float(coords[0].split(',')[2])
        person.longitude = float(coords[0].split(',')[3][:-1])
        person.save()
        return True
    else:
        return False

def address_to_ll(shelter):
    mapbox_key = "access_token=pk.eyJ1IjoidHJpbmlyYWU5MjgiLCJhIjoiY2wxcHYyZjRmMDFqcjNqcXE2Mmd2NXh3eSJ9.7_9DKf4E3PFM0oVNr2KkcA"
    base = "https://api.mapbox.com/geocoding/v5/mapbox.places/"+shelter.address_one+"+"+shelter.city+".json?"
    payload, headers = {}, {}
    req = requests.request("GET", base + mapbox_key, headers=headers, data=payload)
    jsn = json.loads(req.text)
    jsn = jsn['features'][0]['geometry']['coordinates']
    return [float(jsn[1]), float(jsn[0])]

def find_shelter(lat, lon):
    all_stayable = Organization.objects.all().filter(stayable=True)
    closest = None
    shortest_distance = None
    for shelter in all_stayable:
        if closest == None:
            closest = shelter
            coords = address_to_ll(shelter)
            #print("coors = "+coords)
            if coords == False:
                return False
            shortest_distance = get_distance(coords[0], coords[1], lat, lon)
        else:
            coords = address_to_ll(shelter)
            dist = get_distance(coords[0],coords[1], lat, lon)
            if dist < shortest_distance:
                closest = shelter
                shortest_distance = dist
    return closest

def get_distance2(lat1, lon1, lat2, lon2):
    lat, lon = abs(lat1 - lon1), abs(lon1 - lon2)
    return pow((pow(lat, 2) + pow(lon, 2)),.5)

def get_distance(lat1, lon1, lat2, lon2):
    mapbox_key = "access_token=pk.eyJ1IjoidHJpbmlyYWU5MjgiLCJhIjoiY2wxcHYyZjRmMDFqcjNqcXE2Mmd2NXh3eSJ9.7_9DKf4E3PFM0oVNr2KkcA"
    base = "https://api.mapbox.com/directions/v5/mapbox/driving/" + str(lon1) + ',' + str(lat1) + ';' + str(lon2) + ',' + str(lat2) + '?'
    payload, headers = {}, {}
    req = requests.request("GET",base+mapbox_key,headers=headers, data=payload)
    jsn = json.loads(req.text)
    return jsn['routes'][0]['distance']

#using mapbox directions API
def get_directions(slat, slon, dlat, dlon, mode="driving"):
    mapbox_key = "&access_token=pk.eyJ1IjoidHJpbmlyYWU5MjgiLCJhIjoiY2wxcHYyZjRmMDFqcjNqcXE2Mmd2NXh3eSJ9.7_9DKf4E3PFM0oVNr2KkcA"
    base = "https://api.mapbox.com/directions/v5/mapbox/"+mode+"/"+str(slon)+','+str(slat)+';'+str(dlon)+','+str(dlat)+'?'
    additions = "steps=true"
    payload, headers = {}, {}
    req = requests.request("GET",base+additions+mapbox_key,headers=headers, data=payload)
    jsn = json.loads(req.text)
    jsn = jsn['routes'][0]['legs'][0]['steps']
    dirs = []
    for j in jsn:
        dirs.append(j['maneuver']['instruction'])
    return '\n-'.join(dirs)

def translate():
    pass

def help_menu():
    s = "-To change what items you are notified about you can just ask me to “remove” or “add” followed by an item name\n"
    s += '-To get a list of items that I can notify you about, you can just text "items"\n'
    s += '-To change your location, text “change location to” followed by the new zip code or intersection (names of two streets)\n'
    s += '-To find the nearest shelter to you, text “shelter” followed by a intersection you are looking for a shelter near. If you have already given us a location, you can just text “shelter”\n'
    s += '-To get directions to your nearest shelter type text "directions to shelter" you can get walking directions by adding "walking"'
    s += '-You can delete your location information with a text saying "delete location"'
    return s

def change_on_to_true(data):
        if data == "on":
            return True
        else:
            return False