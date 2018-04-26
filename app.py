import requests
import json
import math
from flask import Flask, request, Response

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAAChZCtcdc5kBAMx6uDAEungHTe1bboIlA9Gj8yuKKzYSIddSztboLG3ELUUg6jIKZBDZAKMqpwZAEG5EgWxD7qyeACP8RdiXlzGf07ZChUYsDZAXZAnJsZAL2ZB4E18MdMsZCbjX4cL1dgpmZB38VxVZADBlUV8q5Nefa80q7MOP4VVBa3NbqvNj7yC'
VERIFY_TOKEN = 'anhdeptrainguyhiemnhatvinhbacbo'

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") and request.args.get("hub.challenge"):
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
                return "Verification token mismatch", 403
            return request.args["hub.challenge"], 200

    return "Hello world :v", 200

@app.route('/pycharm')
def forward1():
    return '<h1>Link license server active product of Jestbrain :v</h1>'

@app.route('/pycharm/rpc/obtainTicket.action', methods=['GET', 'POST'])
def forward():
    params = {
        'buildDate': request.args.get('buildDate'),
        'buildNumber': request.args.get('buildNumber'),
        'clientVersion': request.args.get('clientVersion'),
        'hostName': request.args.get('hostName'),
        'machineId': request.args.get('machineId'),
        'productCode': request.args.get('productCode'),
        'productFamilyId': request.args.get('productFamilyId'),
        'salt': request.args.get('salt'),
        'secure': request.args.get('secure'),
        'userName': request.args.get('userName'),
        'version': request.args.get('version'),
        'versionNumber': request.args.get('versionNumber'),
    }
    print(params)
    url = 'http://idea.imsxm.com:80/rpc/obtainTicket.action'
    result = requests.get(url, params=params)
    print(result.status_code)
    print(result.headers)
    print(result.raw)
    return Response(result.content, result.status_code)


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    print(data)
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    send_msg = ''
                    try:
                        message_text = messaging_event["message"]["text"]  # the message's text
                        if (message_text == 'btc'):
                            url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=VND'
                            result = requests.get(url)
                            result = result.json()
                            price = int(math.floor(float(result[0]['price_vnd'])))
                            price = "{:,d}".format(price)
                            send_msg = '1 BTC = ' + result[0]['price_usd'] + ' USD (' + price + ' VND)'
                        else:
                            url = 'http://simsimi.tubotocdo.design/api_sim.php?key=tubotocdo&tenbot=con%20sen%20của%20fpt&text=' + message_text
                            result = requests.get(url)
                            send_msg = result.text
                    except:
                        send_msg = ':)'
                    send_message(sender_id, send_msg)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    print("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.11/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.text + ' --- ' + r.status_code)


if __name__ == '__main__':
    app.run()