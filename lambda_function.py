import json
import requests
import os
from YahooFinance import getLatestPrice, getPortfolio
from portfolio import addTicker, deleteTicker, getTickerByTelegramId
from urllib.parse import quote

TELE_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)

def send_quote(text, chat_id):
    reply = getLatestPrice(text)
    send_message(reply, chat_id)

def add_ticker(text, chat_id, from_id):
    reply = addTicker(from_id, text)
    send_message(reply, chat_id)

def delete_ticker(text, chat_id, from_id):
    reply = deleteTicker(from_id, text)
    send_message(reply, chat_id)

def get_portfolio(chat_id, from_id):
    tickers = getTickerByTelegramId(from_id)
    reply = getPortfolio(tickers)
    send_message(reply, chat_id)

def send_message(message, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(quote(message), chat_id)
    requests.get(url)

def lambda_handler(event, context):
    message = json.loads(event['body'])
    chat_id = message['message']['chat']['id']
    from_id = message['message']['from']['id']
    text = message['message']['text'].split()

    if len(text) == 0:
        send_message("No command entered!", chat_id)
    elif (text[0] == "/quote" and len(text) > 1):
        send_quote(text[1], chat_id)
    elif (text[0] == "/add" and len(text) > 1):
        add_ticker(text[1], chat_id, from_id)
    elif (text[0] == "/delete" and len(text) > 1):
        delete_ticker(text[1], chat_id, from_id)
    elif (text[0] == "/portfolio"):
        get_portfolio(chat_id, from_id)
    else:
        send_message("Invalid command!", chat_id)

    return {
        'statusCode': 200,
        'body': json.dumps('success')
    }