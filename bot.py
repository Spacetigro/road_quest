import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils import executor

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Токен бота не найден! Установите переменную BOT_TOKEN.")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Вопросы викторины по БДД
quiz_data = [
    {
        "question": "Что нужно делать на пешеходном переходе?",
        "options": ["Бежать как можно быстрее", "Пропустить транспорт и перейти дорогу", "Игнорировать машины", "Стоять и смотреть в телефон"],
        "answer": "Пропустить транспорт и перейти дорогу"
    },
    {
        "question": "Что означает красный сигнал светофора?",
        "options": ["Стоп", "Можно идти", "Приготовиться", "Игнорировать"],
        "answer": "Стоп"
    },
    {
        "question": "Какой элемент повышает видимость пешехода ночью?",
        "options": ["Фонарик", "Светоотражающий жилет", "Темная одежда", "Шляпа"],
        "answer": "Светоотражающий жилет"
    },
    {
        "question": "Что делать, если водитель не уступает дорогу на перекрёстке?",
        "options": ["Пройти через него", "Остановиться и ждать", "Кричать на водителя", "Игнорировать правила"],
        "answer": "Остановиться и ждать"
    }
]

user_scores = {}
user_progress = {}

@dp.message_handler(commands=['start'])
async def start_quiz(message: types.Message):
    user_scores[message.from_user.id] = 0
    user_progress[message.from_user.id] = 0
    await message.answer("Привет! Начнём викторину по безопасности дорожного движения.")
    await send_question(message.from_user.id)

async def send_question(user_id):
    idx = user_progress[user_id]
    if idx < len(quiz_data):
        q = quiz_data[idx]
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(*q["options"])
        await bot.send_message(user_id, f"Вопрос {idx+1}:\n{q['question']}", reply_markup=kb)
    else:
        score = user_scores[user_id]
        await bot.send_message(user_id, f"Квиз окончен! 🎉\nТвой результат: {score}/{len(quiz_data)}", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler()
async def check_answer(message: types.Message):
    user_id = message.from_user.id
    idx = user_progress.get(user_id, 0)

    if idx >= len(quiz_data):
        await message.answer("Квиз уже окончен. Напиши /start, чтобы начать заново.")
        return

    q = quiz_data[idx]
    if message.text == q["answer"]:
        user_scores[user_id] += 1
        await message.answer("✅ Верно!")
    else:
        await message.answer(f"❌ Неверно! Правильный ответ: {q['answer']}")
    user_progress[user_id] += 1
    await send_question(user_id)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
