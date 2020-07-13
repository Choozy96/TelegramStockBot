import json
import requests
import os
from YahooFinance import getLatestPrice
from portfolio import addTicker

TELE_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)

def send_quote(text, chat_id):
    reply = getLatestPrice(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(reply, chat_id)
    requests.get(url)

def add_ticker(text, chat_id, from_id):
    reply = addTicker(from_id, text)
    url = URL + "sendMessage?text={}&chat_id={}".format(reply, chat_id)
    requests.get(url)

def lambda_handler(event, context):
    message = json.loads(event['body'])
    chat_id = message['message']['chat']['id']
    from_id = message['message']['from']['id']
    text = message['message']['text']

    add_ticker(text, chat_id, from_id)
    # send_quote(text, chat_id)
    # messageType = text.split()
    # if messageType[0] == '/quote':
    #     body = send_quote(text, chat_id)
    # elif messageType[0] == '/add':

    # else:

    return {
        'statusCode': 200,
        'body': json.dumps('success')
    }