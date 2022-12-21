from requests import request
from .models import Coin
from celery import shared_task

@shared_task
def update_courses():
    with open('coins.txt', encoding="utf-8") as coins:
        response = request('GET', f'https://api.binance.com/api/v3/ticker/price?symbols={coins.read()}')
    coins_courses = response.json()
    for coin in sorted(coins_courses, key=lambda x: x['symbol']):
        Coin.objects.filter(name=coin['symbol'].replace('USDT', '', 1)).update(price=coin['price'])