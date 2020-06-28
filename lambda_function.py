import json
import requests
import os
from YahooFinance import getLatestPrice

TELE_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)

def send_message(text, chat_id):
    reply = getLatestPrice(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(reply, chat_id)
    requests.get(url)

def lambda_handler(event, context):
    message = json.loads(event['body'])
    chat_id = message['message']['chat']['id']
    text = message['message']['text']
    send_message(text, chat_id)
    return {
        'statusCode': 200,
        'body': json.dumps('success')
    }