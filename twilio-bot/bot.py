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

    #adding phone numbers to the texing lists
    if incoming_num not in d['all']:
        d['all'].append(incoming_num) #def a better way to do this
    for key in d:
        if (key in incoming_msg) and (incoming_num not in d[key]):
            d[key].append(incoming_num)


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
