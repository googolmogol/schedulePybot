from datetime import datetime
from threading import Thread
from data_access import *

import telebot
import schedule
import time

bot = telebot.TeleBot("801359509:AAHjuBl_1xRdDHHTTacpT3Q1TSiXl_qQiCw")

chat_id = ''
chat_id_list = []
week = True
lock_is = True


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global chat_id
    chat_id = message.chat.id
    print(message.from_user.first_name, "joined")
    if chat_id not in chat_id_list:
        chat_id_list.append(chat_id)

    hub_btn = button_creating("Хаб с материалами",
                              "https://drive.google.com/drive/folders/16c2M4x1JY1PdvjVngOBrNG29B5Pn5p0o"
                              "?usp=sharing")
    bot.send_message(message.chat.id, '<strong>Здарова студентам!</strong>\N{Victory Hand}\nЯ бот, который будет '
                                      'уведомлять о парах \N{Robot Face}\n ', parse_mode="HTML", reply_markup=hub_btn)


def job():
    global lock_is

    if datetime.today().isoweekday() == 1:
        lock_is = True

    print("Chat_id_list:", chat_id_list)

    print(chat_id)

    send_messages_all("hello", chat_id_list, button_creating("hello", "https://google.com"))


#  creating buttons
def button_creating(text, url):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text=text, url=url)
    markup.add(button)
    return markup


#  function sending messages to all users
def send_messages_all(text, user_list, markup):
    for member in user_list:
        try:
            bot.send_message(member, text, parse_mode="HTML", reply_markup=markup)
        except Exception:
            print("The user has stopped the bot")
            user_list.remove(member)


#  https://qna.habr.com/q/394496
def checker_schedule():
    global lock_is, week
    if datetime.today().isoweekday() == 7 and lock_is:
        if not week:
            week = True
            lock_is = False
        else:
            week = False
            lock_is = False

    if not week:
        get_data("непарний")
    else:
        get_data("парний")

    schedule.every().day.at("00:31").do(job)

    while True:
        if chat_id != '':
            schedule.run_pending()
            time.sleep(1)


#  https://bit.ly/3dnzZbh
#  обязательно нужен новый поток, чтобы не было споров цикла бота и schedule
Thread(target=checker_schedule).start()


def start_bot():
    bot.polling(none_stop=True)


Thread(target=start_bot).start()
