from requests import request
from .models import Coin
from celery import shared_task

@shared_task
def update_courses():
    with open('coins.txt', encoding="utf-8") as coins:
        response = request('GET', f'https://api.binance.com/api/v3/ticker/price?symbols={coins.read()}')
    if response.status_code == 200:
        coins_courses = sorted(response.json(), key=lambda x: x['symbol'])
        coins = list(Coin.objects.all())
        for index in range(len(coins)):
            coins[index].price = coins_courses[index]['price']
        Coin.objects.bulk_update(coins, ['price'])
    else:
        print('API Binance не отвечает')