from threading import Thread

from data_processing import *
from message_handler import message_handler
from parsing_sheet import *

import telebot
import schedule
import time

from reply_keyboard import Keyboard

bot = telebot.TeleBot("801359509:AAHjuBl_1xRdDHHTTacpT3Q1TSiXl_qQiCw")

keyboard = Keyboard(bot)
dataproc = DataProc(bot)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    print(message.from_user.first_name, "joined")
    print("chat_id", chat_id)
    print(chat_id_list)
    if str(chat_id) not in chat_id_list:
        chat_id_list.append(chat_id)
        insert_users(chat_id_list)

    hub_btn = inline_button("Хаб з матеріалами",
                            "https://drive.google.com/drive/folders/16c2M4x1JY1PdvjVngOBrNG29B5Pn5p0o"
                            "?usp=sharing")
    bot.send_message(message.chat.id, '<strong>Здорова студентам!</strong>\N{Victory Hand}\nЯ бот, котрий буде '
                                      'сповіщати вас про пари \N{Robot Face}\n ', parse_mode="HTML",
                     reply_markup=keyboard.main_menu(True, False))
    img = 'https://i.insider.com/5f1ef88ef34d0525d67ebca8'
    bot.send_photo(message.chat.id, img, "Навчальні матеріали", reply_markup=hub_btn)


@bot.message_handler(content_types=['text'])
def send_echo(message):
    message_handler(message, bot)


#  https://qna.habr.com/q/394496
def checker_schedule():
    dataproc.determine_week()
    dataproc.get_full_row()

    schedule.every(2).minutes.do(dataproc.get_full_row)

    while True:
        if len(chat_id_list) > 0:
            schedule.run_pending()
        time.sleep(2)


#  https://bit.ly/3dnzZbh
#  обязательно нужен новый поток, чтобы не было споров цикла бота и schedule


Thread(target=checker_schedule).start()


def start_bot():
    bot.polling(none_stop=True)


Thread(target=start_bot).start()
