import aiohttp
from aiogram import types
from aiogram.dispatcher import filters, FSMContext

from ..bot import dp
from ..keyboards import find_coins, cb_add_monitored_coin, cancel_keyboard, start_keyboard
from ..settings import URL_USERS, URL_MONITORED_COINS
from ..states import AddMonitoredCoinStates

POSITIVE_DECIMAL_REGEXP = r'^(0*[1-9][0-9]*(\.[0-9]*)?|0*\.[0-9]*[1-9][0-9]*)$'


@dp.message_handler(text='Добавить криптовалюту для отслеживания')
async def start_adding_monitored_coin(message: types.Message, state: FSMContext):
    await AddMonitoredCoinStates.user_id.set()
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_USERS + f'?user_id={message.from_user.id}') as response:
            profile = await response.json(content_type=None)
    user_id = profile[0]['id']
    async with state.proxy() as data:
        data['user_id'] = user_id
    await message.answer(
        text='Введите частично, либо полностью название криптовалюты.\nНапример BTC',
        reply_markup=cancel_keyboard)


@dp.message_handler(filters.Text, state=AddMonitoredCoinStates.user_id)
async def show_found_coins(message: types.Message, state: FSMContext):
    keyboard = await find_coins(message.text.upper())
    if len(keyboard["inline_keyboard"]) != 0:
        await message.answer(text='Выберите криптовалюту', reply_markup=keyboard)
        await AddMonitoredCoinStates.next()
    else:
        await message.answer(
            text='К сожалению криптовалюты с таким названием не найдено 😞',
            reply_markup=start_keyboard)
        await state.finish()


@dp.callback_query_handler(cb_add_monitored_coin.filter(), state=AddMonitoredCoinStates.coin_id)
async def expected_price(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['coin_id'] = int(callback_data['coin_id'])
    await AddMonitoredCoinStates.next()
    await callback.message.edit_text(
        text=f'Текущий курс {callback_data["coin_name"]}: {float(callback_data["coin_price"])}$\n'
        f'Введите ожидаемый курс')


@dp.message_handler(regexp=POSITIVE_DECIMAL_REGEXP, state=AddMonitoredCoinStates.expected_price)
async def add_monitored_coin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['expected_price'] = float(message.text)
    monitored_coin_data = {
        'coin_id': data['coin_id'],
        'user_id': data['user_id'],
        'expected_price': data['expected_price']
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(URL_MONITORED_COINS, json=monitored_coin_data) as response:
            if 'non_field_errors' in await response.text():
                await message.answer(
                    text='Данная криптовалюта уже отслеживается!',
                    reply_markup=start_keyboard)
            else:
                await message.answer(
                    text='Криптовалюта успешна добавлена!',
                    reply_markup=start_keyboard)
    await state.finish()


@dp.message_handler(text='Отмена', state='*')
async def cancel_add_monitored_coin(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text='Действие отменено', reply_markup=start_keyboard)
