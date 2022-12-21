from django.core.management import BaseCommand
from requests import request

from coin_app.models import Coin
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Добовление криптовалют в базу данных'

    def handle(self, *args, **kwargs):
        with open('coins.txt', encoding="utf-8") as coins:
            response = request('GET', f'https://api.binance.com/api/v3/ticker/price?symbols={coins.read()}')
            coins_courses = response.json()
        for coin in sorted(coins_courses, key=lambda x: x['symbol']):
            try:
                Coin.objects.create(
                    name=coin['symbol'].replace('USDT', '', 1),
                    price=coin['price'])
            except IntegrityError:
                pass

