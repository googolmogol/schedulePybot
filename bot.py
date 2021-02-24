from threading import Thread
from data_access import *

import telebot
import schedule
import time

from keyboard import Keyboard, button_dict, reply_button, days_dict_ru, items_change_dict, change_values

bot = telebot.TeleBot("801359509:AAHjuBl_1xRdDHHTTacpT3Q1TSiXl_qQiCw")

chat_id_list = get_users_id()
week = False
lock_is = True
global schedule_var, schedule_var2
text_entered = []
lesson_today = []
keyboard = Keyboard(bot)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    print(message.from_user.first_name, "joined")
    if str(chat_id) not in chat_id_list:
        chat_id_list.append(chat_id)
        insert_users(chat_id_list)

    hub_btn = inline_button("Хаб с материалами",
                            "https://drive.google.com/drive/folders/16c2M4x1JY1PdvjVngOBrNG29B5Pn5p0o"
                            "?usp=sharing")
    bot.send_message(message.chat.id, '<strong>Здарова студентам!</strong>\N{Victory Hand}\nЯ бот, который будет '
                                      'уведомлять о парах \N{Robot Face}\n ', parse_mode="HTML",
                     reply_markup=reply_button(['Показать расписание', 'Редактировать расписание']))
    img = 'https://i.insider.com/5f1ef88ef34d0525d67ebca8'
    bot.send_photo(message.chat.id, img, "Учебные материалы", reply_markup=hub_btn)


@bot.message_handler(content_types=['text'])
def send_echo(message):

    if message.text in button_dict:
        keyboard.choose_action(message, message.text)
    elif message.text == 'Показать расписание':
        keyboard.show_schedule(message)
    elif message.text in days_dict_ru:
        keyboard.day_btn(message, message.text)
    elif message.text.isdigit():
        keyboard.lesson_num(message, int(message.text))
    elif message.text in items_change_dict:
        keyboard.change_item(message, message.text)
    elif message.text == 'Сохранить':
        keyboard.update_entered_data(message)
    else:
        change_values.append(message.text)
        print("changes_value in handler:", change_values)


def job(lesson):
    global lock_is

    if datetime.today().isoweekday() == 1:
        lock_is = True

    text = "<strong>Пара: </strong>" + lesson[2] + "\n<strong>Викладач: </strong>" + lesson[3]
    if lesson[2] == '-':
        text = "Сегодня у вас окно!\nПередышка от учёбы!"

    send_messages_all(text, chat_id_list, inline_button("Ссылка на пару", "https://google.com"))


# creating inline buttons
def inline_button(text, url):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text=text, url=url)
    markup.add(button)
    return markup


#  function sending messages to all users
def send_messages_all(text, user_list, markup):
    for member in user_list:
        try:
            bot.send_message(member, text, parse_mode="HTML", reply_markup=markup)
        except Exception as e:
            print(e)
            print("The user has stopped the bot")

            user_list.remove(member)


#  https://qna.habr.com/q/394496
def checker_schedule():
    determine_week()
    get_full_row()

    schedule.every(2).minutes.do(get_full_row)

    while True:
        if len(chat_id_list) > 0:
            schedule.run_pending()
        time.sleep(2)


def determine_week():
    global lock_is, week
    if datetime.today().isoweekday() == 7 and lock_is:
        if not week:
            week = True
            lock_is = False
        else:
            week = False
            lock_is = False


def get_full_row():
    global lesson_today
    if not week:
        lesson_today = get_lessons("непарний", datetime.today().isoweekday())
        print("непарний")
    else:
        lesson_today = get_lessons("парний", datetime.today().isoweekday())
        print("парний")
    send_schedule()


# sending schedule
def send_schedule():
    global schedule_var, schedule_var2
    # stop earlier schedules
    try:
        schedule.cancel_job(schedule_var)
        schedule.cancel_job(schedule_var2)
    except Exception as e:
        print(e, "The previous schedule wasn't created!")
    try:
        for i in lesson_today:
            schedule_var = schedule.every().day.at(i[1]).do(job, i)
            if i[2] != '-':
                text = '<strong>Напоминание!</strong>\nПара "' + i[2] + '" начнётся через 10 минут.'
                schedule_var2 = schedule.every().day.at(time_before_lesson(i[1])).do(send_messages_all, text,
                                                                                     chat_id_list,
                                                                                     reply_button(
                                                                                         ['Показать расписание',
                                                                                          'Изменить расписание']))
    except Exception as e:
        print(e, "Invalid time format")

#  https://bit.ly/3dnzZbh
#  обязательно нужен новый поток, чтобы не было споров цикла бота и schedule


Thread(target=checker_schedule).start()


def start_bot():
    bot.polling(none_stop=True)


Thread(target=start_bot).start()
