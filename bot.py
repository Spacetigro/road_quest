import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Токен бота не найден! Установите переменную BOT_TOKEN.")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Бот работает ✅")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
