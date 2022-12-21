import aiohttp
from aiogram import types

from ..bot import dp
from ..settings import URL_MONITORED_COINS, URL_USERS


@dp.message_handler(text='Показать все отслеживаемые криптовалюты')
async def show_monitored_coins(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_USERS + f'?user_id={message.from_user.id}') as response:
            profile = await response.json()
        profile_id = profile[0]['id']
        async with session.get(URL_MONITORED_COINS + f'?user_id={profile_id}') as response:
            monitored_coins = await response.json()
    if len(monitored_coins) != 0:
        monitored_coins = [
            f'Криптовалюта {coin["coin_name"]}\n' \
            f'Текущая цена {float(coin["coin_price"])}$\n' \
            f'Ожидаемая цена {float(coin["expected_price"])}$'
            for coin in monitored_coins
            ]
        await message.answer(text="\n\n".join(monitored_coins))
    else:
        await message.answer(text='У Вас нет отслеживаемых криптовалют 😞')
