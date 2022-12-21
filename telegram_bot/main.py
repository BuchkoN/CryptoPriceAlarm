import bot.bot_func
from aiogram.utils import executor
from bot.bot import dp

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
