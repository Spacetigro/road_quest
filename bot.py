import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils import executor

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Токен бота не найден! Установите переменную BOT_TOKEN.")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

quiz_data = [
    {
        "question": "Какой язык программирования используется в этом боте?",
        "options": ["Python", "Java", "C++", "Pascal"],
        "answer": "Python"
    },
    {
        "question": "Сколько бит в 1 байте?",
        "options": ["4", "8", "16", "32"],
        "answer": "8"
    },
    {
        "question": "Кто создал Telegram?",
        "options": ["Илон Маск", "Павел Дуров", "Билл Гейтс", "Марк Цукерберг"],
        "answer": "Павел Дуров"
    }
]

user_scores = {}
user_progress = {}
user_questions = {}

@dp.message_handler(commands=['start'])
async def start_quiz(message: types.Message):
    user_scores[message.from_user.id] = 0
    user_progress[message.from_user.id] = 0
    shuffled = quiz_data.copy()
    random.shuffle(shuffled)
    user_questions[message.from_user.id] = shuffled
    await message.answer("Привет! Это викторина. Чтобы начать заново, введи /start.
Помощь: /help")
    await send_question(message.from_user.id)

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer("Это бот для викторин.
Команды:
/start — начать викторину
/help — помощь")

async def send_question(user_id):
    idx = user_progress[user_id]
    questions = user_questions[user_id]
    if idx < len(questions):
        q = questions[idx]
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(*q["options"])
        await bot.send_message(user_id, f"Вопрос {idx+1}:
{q['question']}", reply_markup=kb)
    else:
        score = user_scores[user_id]
        await bot.send_message(user_id, f"Квиз окончен! 🎉
Твой результат: {score}/{len(quiz_data)}", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler()
async def check_answer(message: types.Message):
    user_id = message.from_user.id
    idx = user_progress.get(user_id, 0)

    if user_id not in user_questions or idx >= len(user_questions[user_id]):
        await message.answer("Квиз уже окончен. Напиши /start, чтобы начать заново.")
        return

    q = user_questions[user_id][idx]
    if message.text == q["answer"]:
        user_scores[user_id] += 1
        await message.answer("✅ Верно!")
    else:
        await message.answer(f"❌ Неверно! Правильный ответ: {q['answer']}")
    user_progress[user_id] += 1
    await send_question(user_id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
