import telebot
from telebot import types

bot= telebot.TeleBot('8221673982:AAH2PwHmXv1Rl4WMkmpZUpPffaRn2lQTtWU')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет")
