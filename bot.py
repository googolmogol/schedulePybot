from threading import Thread

from data_processing import *
from parsing_sheet import *

import telebot
import schedule
import time

from reply_keyboard import Keyboard

bot = telebot.TeleBot("801359509:AAHjuBl_1xRdDHHTTacpT3Q1TSiXl_qQiCw")

chat_id_list = get_users_id()
week = False
lock_is = True
global schedule_var, schedule_var2
text_entered = []
lesson_today = []
keyboard = Keyboard(bot)


def status_user(value):
    if value == "Вибрати дію":
        if user_step["action"] == "Редагувати пару" or user_step["action"] == "Видалити пару" or user_step["action"] \
                == "Додати пару":
            return True
        else:
            return False
    if value == "Вибрати тиждень":
        if user_step["action"] == "Редагувати пару" or user_step["action"] == "Видалити пару" or user_step["action"] \
                == "Додати пару" or user_step["week"] == "Парний" or user_step["week"] == "Непарний":
            return True
        else:
            return False
    if value == "Вибрати день":
        if user_step["action"] == "Редагувати пару" or user_step["action"] == "Видалити пару" or user_step["action"] \
                == "Додати пару" or user_step["week"] == "Парний" or user_step["week"] == "Непарний" or \
                user_step["day"] == "Понеділок" or user_step["day"] == "Вівторок" or user_step["day"] == "Середа" or \
                user_step["day"] == "Четвер" or user_step["day"] == "П'ятниця" or user_step["day"] == "Субота" or \
                user_step["day"] == "Неділя":
            return True
        else:
            return False


def clear_user_step(current):
    keys = list(user_step.keys())[::-1]  # reverse list
    for i in keys:
        user_step[i] = '-'
        if i == current:
            break


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    print(message.from_user.first_name, "joined")
    if str(chat_id) not in chat_id_list:
        chat_id_list.append(chat_id)
        insert_users(chat_id_list)

    hub_btn = inline_button("Хаб з матеріалами",
                            "https://drive.google.com/drive/folders/16c2M4x1JY1PdvjVngOBrNG29B5Pn5p0o"
                            "?usp=sharing")
    bot.send_message(message.chat.id, '<strong>Здорова студентам!</strong>\N{Victory Hand}\nЯ бот, котрий буде '
                                      'сповіщати вас про пари \N{Robot Face}\n ', parse_mode="HTML",
                     reply_markup=keyboard.main_menu(True))
    img = 'https://i.insider.com/5f1ef88ef34d0525d67ebca8'
    bot.send_photo(message.chat.id, img, "Навчальні матеріали", reply_markup=hub_btn)


@bot.message_handler(content_types=['text'])
def send_echo(message):
    if message.text == 'Показати розклад':
        keyboard.show_schedule(message)

    if message.text == 'Головне меню':
        bot.send_message(message.chat.id, message.text, parse_mode="HTML", reply_markup=keyboard.main_menu(True))
        clear_user_step("action")

    if message.text == "Редагувати розклад" or message.text == "Назад в меню редагування розкладу":
        keyboard.edit_schedule(message)
        clear_user_step("action")

    if message.text == "Редагувати пару" or message.text == "Видалити пару":
        keyboard.edit_lesson(message)
        user_step["action"] = message.text

    if message.text == "Парний" or message.text == "Непарний":
        if status_user("Вибрати дію"):
            keyboard.choosing_day(message)
            user_step["week"] = message.text
        else:
            bot.send_message(message.chat.id, "Сталися технічні зміни\nПоверніться до головного меню або перезапустіть "
                                              "бот", parse_mode="HTML", reply_markup=keyboard.main_menu(False))

    if message.text in days_dict_ua:
        if status_user("Вибрати тиждень"):
            keyboard.choosing_lesson(message)
            user_step["day"] = message.text
        else:
            bot.send_message(message.chat.id, "Сталися технічні зміни\nПоверніться до головного меню або перезапустіть "
                                              "бот", parse_mode="HTML", reply_markup=keyboard.main_menu(False))

    if message.text.isdigit() and message.text in button_list:
        if status_user("Вибрати день"):
            keyboard.choosing_lesson_num(message)
            user_step["lesson_num"] = message.text
        else:
            bot.send_message(message.chat.id, "Сталися технічні зміни\nПоверніться до головного меню або перезапустіть "
                                              "бот", parse_mode="HTML", reply_markup=keyboard.main_menu(False))

    # go back buttons

    if message.text == "Назад до вибору тижня":
        keyboard.edit_lesson(message)
        clear_user_step("week")

    if message.text == "Назад до вибору дня":
        keyboard.choosing_day(message)
        clear_user_step("day")


    print(user_step)


def job(lesson):
    global lock_is

    if datetime.today().isoweekday() == 1:
        lock_is = True

    text = "<strong>Пара: </strong>" + lesson[2] + "\n<strong>Викладач: </strong>" + lesson[3]
    if lesson[2] == '-':
        text = "Сьогодні у вас вікно!\nПерепочинок від навчання!"

    send_messages_all(text, chat_id_list, inline_button("Посилання на пару", "https://google.com"))


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
        lesson_today = get_lessons_row("непарний", datetime.today().isoweekday(), False)
        print("непарний")
        print(lesson_today)
    else:
        lesson_today = get_lessons_row("парний", datetime.today().isoweekday(), False)
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
                text = '<strong>Нагадування!</strong>\nПара "' + i[2] + '" розпочнеться за 10 хвилин.'
                schedule_var2 = schedule.every().day.at(time_before_lesson(i[1])).do(send_messages_all, text,
                                                                                     chat_id_list,
                                                                                     keyboard.main_menu)
    except Exception as e:
        print(e, "Invalid time format")

#  https://bit.ly/3dnzZbh
#  обязательно нужен новый поток, чтобы не было споров цикла бота и schedule


Thread(target=checker_schedule).start()


def start_bot():
    bot.polling(none_stop=True)


Thread(target=start_bot).start()
