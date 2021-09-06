import telebot
from telebot import types
from RTDB import RTDB

BOT = telebot.TeleBot("YourTelegramBotToken")

def create_buttons(dictionary, key, answers):
    markup = types.InlineKeyboardMarkup()
    for i in answers:
        if i != None:
            button = types.InlineKeyboardButton(text=i, callback_data=i)
            markup.add(button)
    return markup