from asyncio import create_task, sleep

import aiohttp
from aioschedule import every, run_pending

from ..bot import dp
from ..settings import URL_MONITORED_COINS


async def send_notifications():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_MONITORED_COINS) as response:
            monitored_coins = await response.json()
        for monitored_coin in monitored_coins:
            if float(monitored_coin['coin_price']) <= float(monitored_coin['expected_price']):
                await dp.bot.send_message(
                    chat_id=monitored_coin['telegram_profile'],
                    text=f'Криптовалюта {monitored_coin["coin_name"]} достигла ожидаемого курса:\n'
                    f'Ожидаемый курс {float(monitored_coin["expected_price"])}$\n'
                    f'Текущий курс {float(monitored_coin["coin_price"])}$\n'
                    f'Удачной покупки 😉')
                await session.delete(URL_MONITORED_COINS + f'{monitored_coin["id"]}')


async def scheduler():
    every(30).seconds.do(send_notifications)
    while True:
        await run_pending()
        await sleep(0.1)


async def on_startup(_):
    create_task(scheduler())
