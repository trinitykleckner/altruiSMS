import requests
from flask import *
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms():

    incoming = request.values.get('Body', '').lower()
    to_number = request.values.get('From')
    url = "https://www.themealdb.com/api/json/v1/1/search.php?s=" + incoming

    response = requests.request("GET", url).json()

    #CREATE A PERSON OBJECT

    r = ""
    #adding to and removing from the data base
    items = ["food", "diaper", "blanket", "sanitary"]
    if new(to_number):
        add_num(to_number)
        r = "Hi! I’m chatbot, I am here to help you get access to the resources you need. By responding to this text you can opt into receiving notifications as local organizations are holding drives, or giving away specific items. The items you can choose to be notified about are food, diapers, blankets, and sanitary items. Reply to this text with the names of the items you wish to be notified about in the future."
    else:
        if item == "help":
            r = help_menu()
        for item in items:
            rem = "remove "+item
            if (rem in incoming):
                remove_num(to_number, item)
                r += "Sounds good, I will no longer notify you about avalible "+item+"\n"
            elif (item in incoming):
                add_num(to_number, item)
                r += "Sounds good! To make sure we are notifying you about distributions of "+item+" in your area please reply to this text with either the word “zip” followed by a zip code near you or the word “intersection” followed by names of two intersecting streets near you\n"

        if "shelter" in incoming:
            if person.location == None:
                r = 'To find a shelter for you I need some idea of your location, send a message saying "shelter" followed by either "zip" and a zip code, or "intersection" and the name of two streets that intersect near you'

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
                r += "Thanks!! You will now be notified when there is a distribution near you."
            else:
                r += 'Hm, I could not find that intersection, could you try entering another one (make sure to include the word "intersection" before the street names)'

        if r == "":
            r = "I'm sorry, I'm not sure what that means, for a full list of things I can do text \"help\""



    client = Client("AC86f5c09c4f505b9a005468ffcf760039","3c47e7ec29619f8f27c6a11115a5d433")

    message = client.messages \
        .create(
            body=r,
            from_='+18126055840',    #sams: '+15854407446',
            to= to_number
        )

    print(message.sid)
    return message.sid

#adds a number to which list
def add_num(num, which="master"):
    if new(num, which): #dont do anything num in list
        return True

#removes a number from which
def remove_num(num, which="master"):
    if not new(num, which): #dont do anything if the num isnt in which
        return True

#returns true if num not in which phone list
def new(num, which="master"):
    return False

#returns true if found intersection
def intersect_valid(road1, road2):
    return True

def help_menu():
    s = "-To change what items you are notified about you can just ask me to “remove” or “add” followed by an item name\n"
    s += '-To get a list of items that I can notify you about, you can just text "items"\n'
    s += '-To change your location, text “change location to” followed by the new zip code or intersection (names of two streets)\n'
    s += '-To find the nearest shelter to you, text “shelter” followed by a zip code or intersection you are looking for a shelter near. If you have already given us a location, you can just text “shelter”\n'
    return s

if __name__ == "__main__":
    app.run(debug=True)
