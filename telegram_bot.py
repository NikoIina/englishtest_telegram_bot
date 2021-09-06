import os
import telebot
from telebot import types
import pyrebase
from RTDB import RTDB
from utils import create_buttons
from flask import Flask, request

# НАСТРОЙКИ БОТА

TOKEN = "YourTelegramBotToken"

BOT = telebot.TeleBot(TOKEN)

server = Flask(__name__)

# БОТ

botDB = RTDB()

@BOT.message_handler(commands=['start'])
def start_command(message):
    BOT.send_message(
        message.chat.id,
        'Welcome to English test! ' + '\n'
        'To start test send /test ' + '\n'
        'To get help send /help'
    )

@BOT.message_handler(commands=['help'])
def help_command(message):
    BOT.send_message(
        message.chat.id,
        '1) Start your English efficiency test with /test' +'\n'
        '2) Contact me at your-email@gmail.com'
    )

# СТАРТ ТЕСТА

@BOT.message_handler(commands=['test'])
def start_test(message):
    botDB.create_list()
    question_key = botDB.questions[botDB.index]
    check_all(message, question_key)

# ОБРАБОТКА ОТВЕТА

@BOT.callback_query_handler(func=lambda call: True)
def handle_query(call):
    botDB.count_points(botDB.questions[botDB.index],call)
    if botDB.index < len(botDB.dict):
        question_key = botDB.questions[botDB.index]
        check_all_call(call.message, question_key, call)
    if botDB.index == len(botDB.dict):
        BOT.send_message(call.message.chat.id, sum(botDB.points))

@BOT.message_handler(content_types=['text'])
def no_butt_message(message):
    botDB.count_points_text(botDB.questions[botDB.index],message.text)
    if botDB.index < len(botDB.dict):
        question_key = botDB.questions[botDB.index]
        check_all(message, question_key)
    if botDB.index == len(botDB.dict):
        BOT.send_message(message.chat.id, sum(botDB.points))

def check_all(message, key):
    question = botDB.create_question(key)
    if botDB.get_answers(key):
        markup = create_buttons(botDB.dict, key, botDB.get_answers(key))
        if botDB.get_picture(key):
            BOT.send_photo(message.chat.id, botDB.get_picture(key))
        if botDB.get_audio(key):
            BOT.send_audio(message.chat.id, botDB.get_audio(key))
        BOT.send_message(message.chat.id, question, reply_markup=markup)
    else:
        if botDB.get_picture(key):
            BOT.send_photo(message.chat.id, botDB.get_picture(key))
        if botDB.get_audio(key):
            BOT.send_audio(message.chat.id, botDB.get_audio(key))
        BOT.send_message(message.chat.id, question)

def check_all_call(message, key, call):
    question = botDB.create_question(key)
    if botDB.get_answers(key):
        markup = create_buttons(botDB.dict, key, botDB.get_answers(key))
        if botDB.get_picture(key):
            BOT.send_photo(call.message.chat.id, botDB.get_picture(key))
        if botDB.get_audio(key):
            BOT.send_audio(call.message.chat.id, botDB.get_audio(key))
        BOT.send_message(call.message.chat.id, question, reply_markup=markup)
    else:
        if botDB.get_picture(key):
            BOT.send_photo(call.message.chat.id, botDB.get_picture(key))
        if botDB.get_audio(key):
            BOT.send_audio(call.message.chat.id, botDB.get_audio(key))
        BOT.send_message(call.message.chat.id, question)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    BOT.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    BOT.remove_webhook()
    BOT.set_webhook(url=f"https://your-app-name.herokuapp.com/{TOKEN}")
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))