import requests
from flask import *
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms():

    food = request.values.get('Body', '').lower()
    to_number = request.values.get('From')
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


if __name__ == "__main__":
    app.run(debug=True)
