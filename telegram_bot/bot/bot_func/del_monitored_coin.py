import aiohttp
from aiogram import types

from ..bot import dp
from ..keyboards import del_coin, cb_del_monitored_coin
from ..settings import URL_MONITORED_COINS


@dp.message_handler(text='Удалить отслеживаемую криптовалюту')
async def show_deleted_coins(message: types.Message):
    keyboard = await del_coin(message.from_user.id)
    if len(keyboard["inline_keyboard"]) != 0:
        await message.answer(
            text='Выберете криптовалюту, которую хотите удалить',
            reply_markup=keyboard)
    else:
        await message.answer(text='У Вас нет отслеживаемых криптовалют 😞')

@dp.callback_query_handler(cb_del_monitored_coin.filter())
async def del_monitored_coin(callback: types.CallbackQuery, callback_data: dict):
    async with aiohttp.ClientSession() as session:
        await session.delete(URL_MONITORED_COINS + f'{callback_data["id"]}')
    await callback.message.edit_text(
        text=f'Криптовалюта {callback_data["coin_name"]} больше не отслеживается')
