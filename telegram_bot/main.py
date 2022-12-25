import bot.bot_func
from aiogram.utils import executor
from bot.bot import dp
from bot.bot_func.send_notifications import on_startup

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
