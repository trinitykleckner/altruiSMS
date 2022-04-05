from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    incoming_num = request.values.get('From') #need to check if this has spec chars
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    d = {'all':[], 'food':[], 'diapers':[], 'coat':[], 'blanket':[]}

    #adding and removing phone numbers to the texing lists
    if incoming_num not in d['all']:
        d['all'].append(incoming_num) #def a better way to do this
        msg.body('Thanks! Just so we know where is local to you, respond to this \
        message with the word "location" followed by the name of two streets that \
        intersect near you')
        responded = True
    for key in d:
        rem = "remove "+key
        if (rem in incoming_msg) and (incoming_num in d[key]):
            d[key].remove(incoming_num)
        elif (key in incoming_msg) and (incoming_num not in d[key]):
            d[key].append(incoming_num)
    if location in incoming_msg:
        print(0)
        #NEED TO DO
        msg.body('Great!! You’ll get a text when the items you selected are being \
        distributed near you. If you ever want to add an item to be notified about,\
        just send a text with the name of that item. If you ever want to no longer\
        be notified for an item just send a text saying “remove” followed by the name \
        of the item. (example: “remove diapers”)')
        responded = True



    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body("Hm, I'm not sure what you mean")
    return str(resp)


if __name__ == '__main__':
    app.run()
