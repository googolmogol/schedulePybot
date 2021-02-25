from datetime import datetime

import schedule

from parsing_sheet import get_lessons_row, time_before_lesson, get_users_id
from reply_keyboard import inline_button, Keyboard

# dict for user activity, to track his steps
user_step = {"action": '-', "week": '-', "day": '-', "lesson_num": '-', "item_to_change": '-'}
# dict with change items and their position on Google SH
items_change_dict = {'Назву пари': 2, 'Викладача': 3, 'Час': 1, 'Посилання': 5, 'Тиждень': 4}

days_dict_ua = {'Понеділок': 1, 'Вівторок': 2, 'Середа': 3, 'Четвер': 4, "П'ятниця": 5, 'Субота': 6, 'Неділя': 7}

button_list = []  # list for creating dynamic buttons
lesson_to_change1 = []  # list to save nedeed rows
chat_id_list = get_users_id()  # list to determine user is new or no
week = False  # current week
lock_is = True  # var for week changing
global schedule_var, schedule_var2  # vars for schedules
killer_var = [False]
lesson_today = []  # list for parsing today's lessons


# get all lessons for choosen day
def get_lesson_to_change(ch_week, day):
    day_digit = days_dict_ua[day]
    button_list.clear()
    text = day + ", пари, " + ch_week.lower() + " тиждень:\n\n"
    global lesson_to_change1
    lesson_to_change1 = get_lessons_row(ch_week.lower(), day_digit, True)
    counter = 1
    for i in lesson_to_change1:
        text += str(counter)
        counter += 1
        button_list.append(str(counter - 1))

        text += ". Пара: " + i[2] + "\nВикладач: " + i[3] + "\nЧас: " + i[1] + "\nПосилання: " + '<a href="' + i[5] + \
                '">лінк</a>\nТиждень: ' + i[4]

        text += '\n'
    text += "\nОберіть номер пари, яку необхідно редагувати: "
    button_list.append('Назад до вибору дня')
    button_list.append('Головне меню')
    return button_list, text


# chosing needed lesson
def get_text_choosing_lesson_num(message):
    index = int(message.text)
    text = '\n'
    text += "Пара: " + lesson_to_change1[index - 1][2] + "\nВикладач: " + lesson_to_change1[index - 1][
        3] + "\nЧас: " + lesson_to_change1[index - 1][1] + "\nПосилання: " + '<a href="' + \
        lesson_to_change1[index - 1][5] + '">лінк</a>\nТиждень: ' + lesson_to_change1[index - 1][4]
    text += '\n'
    text += "\nОберіть, що саме необхідно редагувати:"
    return text


class DataProc:

    def __init__(self, bot):
        self.bot = bot

    # reminds about today's lesson
    def job(self, lesson):
        global lock_is

        if datetime.today().isoweekday() == 1:
            lock_is = True

        text = "<strong>Пара: </strong>" + lesson[2] + "\n<strong>Викладач: </strong>" + lesson[3]
        if lesson[2] == '-':
            text = "Сьогодні у вас вікно!\nПерепочинок від навчання!"

        self.send_messages_all(text, chat_id_list, inline_button("Посилання на пару", lesson[5]))

    #  function sending messages to all users
    def send_messages_all(self, text, user_list, markup):
        for member in user_list:
            try:
                self.bot.send_message(member, text, parse_mode="HTML", reply_markup=markup)
            except Exception as e:
                print(e)
                print("The user has stopped the bot")

                user_list.remove(member)

    # define current week
    @staticmethod
    def determine_week():
        global lock_is, week
        if datetime.today().isoweekday() == 7 and lock_is:
            if not week:
                week = True
                lock_is = False
            else:
                week = False
                lock_is = False

    # request data from google sheet
    def get_full_row(self):
        global lesson_today
        if not week:
            lesson_today = get_lessons_row("непарний", datetime.today().isoweekday(), False)
       #     print("непарний")
      #      print(lesson_today)
        else:
            lesson_today = get_lessons_row("парний", datetime.today().isoweekday(), False)
     #       print("парний")
        self.send_schedule()

    # sending schedule
    def send_schedule(self):
        global schedule_var, schedule_var2
        keyb = Keyboard(self)
        markup = keyb.main_menu(False, True)
        # stop earlier schedules
        try:
            schedule.cancel_job(schedule_var)
            schedule.cancel_job(schedule_var2)
        except Exception as e:
            print(e, "The previous schedule wasn't created!")
        try:
            for i in lesson_today:
                schedule_var = schedule.every().day.at(i[1]).do(self.job, i)
                if i[2] != '-':
                    text = '<strong>Нагадування!</strong>\nПара "' + i[2] + '" розпочнеться за 10 хвилин.'
                    schedule_var2 = schedule.every().day.at(time_before_lesson(i[1])).do(self.send_messages_all, text,
                                                                                         chat_id_list, markup)
        except Exception as e:
            print(e, "Invalid time format")


# verifies compliance with the sequence of user steps
def status_user(value):
    if value == "Вибрати дію":
        if user_step["action"] != "-":
            return True
        else:
            return False
    if value == "Вибрати тиждень":
        if user_step["action"] != "-" and user_step["week"] != "-":
            return True
        else:
            return False
    if value == "Вибрати день":
        if user_step["action"] != "-" and user_step["week"] != "-" and user_step["day"] != "-":
            return True
        else:
            return False


# clear user status
def clear_user_step(current):
    keys = list(user_step.keys())[::-1]  # reverse list
    for i in keys:
        user_step[i] = '-'
        if i == current:
            break


# https://clck.ru/TSmqM
# break function
def killer_fun(var):
    if var:
        killer_var[0] = False
        raise Exception
