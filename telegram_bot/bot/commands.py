from aiogram import types
import aiohttp

from .bot import dp
from .keyboards import start_keyboard
from .settings import URL_USERS


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(
        'Моя единственная задача, это сообщить, когда курс криптовалюты опустится до нужного тебе значения.\n'
        'Курс криптовалют соответсвует рыночному курсу на бирже Binance.\n'
        'Со списком доступных криптовалют можно ознакомиться на [Binance](https://www.binance.com/ru/markets/).\n'
        'Я умею отслеживать множество криптовалют одновременно.\n'
        'Для того, чтобы начать со мной работать, введи команду /start и следуй простым инструкциям 👌',
        parse_mode='Markdown',
        disable_web_page_preview=True
    )


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    data = {
        'user_id': message.from_user.id,
        'username': message.from_user.username if message.from_user.username is not None else ""
    }
    async with aiohttp.ClientSession() as session:
        await session.post(URL_USERS, json=data)
    await message.answer(text='Выбери действие ⬇️', reply_markup=start_keyboard)
