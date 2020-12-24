import requests
import time
import os
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
from dotenv import load_dotenv
load_dotenv()

cmc = CoinMarketCapAPI(os.getenv("API_KEY"))
WEBHOOK_URL_KEY = os.getenv("WEBHOOK_URL_KEY")
WEBHOOK_URL = f'https://maker.ifttt.com/trigger/price_emergency/with/key/{WEBHOOK_URL_KEY}'
symbol = input('Which cryptocurrency do you want to receive notifications about (like BTC, ETH, XPR etc.): ')


def get_latest_price():
    r = cmc.cryptocurrency_quotes_latest(symbol={symbol})
    price = r.data[symbol]['quote']['USD']['price']
    return "{:.5f}".format(price)


def post_ifttt_webhook(event, value):
    data = {'value1': symbol,
            'value2': value}
    ifttt_event_url = WEBHOOK_URL.format(event)
    requests.post(ifttt_event_url, json=data)


def main():
    price = get_latest_price()
    alert_price = "{:.5f}".format(float(input('At what price would you like us to alert you: ')))
    while True:
        if price >= alert_price:
            post_ifttt_webhook('price_emergency', price)
        time.sleep(5*60)


if __name__ == "__main__":
    main()
