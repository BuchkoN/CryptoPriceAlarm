from aiogram.dispatcher.filters.state import StatesGroup, State


class AddMonitoredCoinStates(StatesGroup):
    user_id = State()
    coin_id = State()
    expected_price = State()
