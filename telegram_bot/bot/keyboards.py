import aiohttp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from .settings import URL_COINS, URL_USERS, URL_MONITORED_COINS

cb_add_monitored_coin = CallbackData('found_coins_keyboard', 'coin_id',
                                     'coin_name', 'coin_price')
cb_del_monitored_coin = CallbackData('del_coins_keyboard', 'id', 'coin_name')


# Клавиатура команды /start
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Добавить криптовалюту для отслеживания')],
        [KeyboardButton(text='Показать все отслеживаемые криптовалюты')],
        [KeyboardButton(text='Удалить отслеживаемую криптовалюту')]
    ],
    resize_keyboard=True
)


# Клавиатура отмены
cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Отмена')]],
    resize_keyboard=True
)


# Клавиатура с найденными криптовалютами
async def find_coins(name):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_COINS) as response:
            found_coins = await response.json()
    buttons = [
        InlineKeyboardButton(
            text=coin['name'],
            callback_data=cb_add_monitored_coin.new(coin['id'], coin['name'], coin['price']))
        for coin in found_coins if name in coin['name']
    ]
    found_coins_keyboard = InlineKeyboardMarkup(row_width=1).add(*buttons)
    return found_coins_keyboard


# Клавиатура удаления криптовалюты
async def del_coin(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_USERS + f'?user_id={user_id}') as response:
            profile = await response.json()
        profile_id = profile[0]['id']
        async with session.get(URL_MONITORED_COINS + f'?user_id={profile_id}') as response:
            monitored_coins = await response.json()
    buttons = [
        InlineKeyboardButton(
            text=coin['coin_name'],
            callback_data=cb_del_monitored_coin.new(coin['id'], coin['coin_name']))
        for coin in monitored_coins
    ]
    del_monitored_coin = InlineKeyboardMarkup(row_width=1).add(*buttons)
    return del_monitored_coin
