import telebot

from data_access import *

# dicts instead switch/if-else

# dict of buttons, last value - text to send
button_dict = {
    "Редактировать расписание": ['Добавить пару', 'Изменить пару', 'Удалить пару', 'Главное меню',
                                 'Выберите действие'],
    "Назад в редактирование расписания": ['Добавить пару', 'Изменить пару', 'Удалить пару', 'Главное меню',
                                          'Выберите действие'],
    "Главное меню": ['Показать расписание', 'Редактировать расписание', 'Вот мы и вернулись'],
    "Изменить пару": ['Четная', 'Нечетная', 'Назад в редактирование расписания', 'Выберите неделю'],
    "Удалить пару": ['Четная', 'Нечетная', 'Назад в редактирование расписания', 'Выберите неделю'],
    "Назад в выбор недели": ['Четная', 'Нечетная', 'Назад в редактирование расписания', 'Главное меню',
                             'Выберите неделю'],
    "Четная": ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье',
               'Назад в выбор недели', 'Главное меню', 'Выберите день'],
    "Нечетная": ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье',
                 'Назад в выбор недели', 'Главное меню', 'Выберите день'],
    "Назад в выбор дня": ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье',
                          'Назад в выбор недели', 'Главное меню', 'Выберите день'],
    "Назад в выбор параметра для изменения": ['Название пары', 'Преподавателя', 'Время', 'Ссылку',
                                              'Выберите, что нужно изменить'],

}

days_dict_ru = {'Понедельник': 1, 'Вторник': 2, 'Среда': 3, 'Четверг': 4, 'Пятница': 5, 'Суббота': 6, 'Воскресенье': 7}

items_change_dict = {'Название пары': 2, 'Преподавателя': 3, 'Время': 1, 'Ссылку': 5}

# list which holds values to change:
# [0] - row
# [1] - col
# [2] - value to change
change_values = []

changed_week = ''  # var to define which week choose user


# creating reply button
def reply_button(btn_list):
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    for i in btn_list:
        markup.row(i)
    return markup


# noinspection PyGlobalUndefined
class Keyboard:

    def __init__(self, bot):
        self.bot = bot

    # just send photo of schedule
    def show_schedule(self, message):
        img = open('restfiles/schedule.jpg', 'rb')
        self.bot.send_photo(message.chat.id, img, "Ваше расписание")

    # universal fun
    def choose_action(self, message, key):
        global changed_week
        if message.text == 'Четная':
            changed_week = "парний"
        elif message.text == 'Нечетная':
            changed_week = "непарний"

        text = button_dict[key][-1]
        button_list = button_dict[key][:-1]
        self.bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=reply_button(button_list))

    # determinate which lessons is on the day
    def day_btn(self, message, day_txt):
        day = days_dict_ru[day_txt]
        print("day in day_btn:", day)
        text = day_txt + ", пары," + changed_week + "неделя:\n\n"
        global lesson_to_change
        lesson_to_change.clear()

        lesson_to_change = get_lessons(changed_week, day)
        print(lesson_to_change)
        counter = 1
        button_list = []
        for i in lesson_to_change:
            text += str(counter)
            counter += 1
            button_list.append(str(counter - 1))

            text += ". Пара: " + i[2] + "\nВикладач: " + i[3] + "\nЧас: " + i[1]

            text += '\n'
        text += "\nВыберите какую нужно изменить:"
        button_list.append('Назад в выбор дня')
        button_list.append('Главное меню')
        print("btn_list in day_btn: ", button_list)
        self.bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=reply_button(button_list))

    # sending chosen lesson to change to user
    def lesson_num(self, message, index):
        change_values.clear()
        print("lesson_to_change in lesson_num", lesson_to_change)
        text = '\n'
        text += "Пара: " + lesson_to_change[index - 1][2] + "\nВикладач: " + lesson_to_change[index - 1][
            3] + "\nЧас: " + lesson_to_change[index - 1][1]
        text += '\n'
        text += "\nВыберите, что нужно изменить:"
        button_list = ['Название пары', 'Преподавателя', 'Время', 'Ссылку', 'Выберите, что нужно изменить']
        change_values.append(row_index_to_change[index - 1])  # add row on google sheet of choosen lesson

        self.bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=reply_button(button_list))

    # user choosing data to change
    def change_item(self, message, text):
        change_values.append(items_change_dict[text] + 1)  # add col on google sheet of choosen lesson
        text = 'Введите ' + text.lower() + ' и нажмите конпку "Сохранить"'
        button_list = ['Сохранить', 'Главное меню']
        self.bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=reply_button(button_list))

    # save changes on google sheet
    def update_entered_data(self, message):
        try:
            update_data(change_values[0], change_values[1], change_values[2])
            print("changed_values in update_entered_data:", change_values)
            temp = change_values[0]
            change_values.clear()
            change_values.append(temp)
            self.bot.send_message(message.chat.id, "Сохранил", parse_mode="HTML", reply_markup=reply_button(
                ['Назад в выбор параметра для изменения', 'Назад в выбор дня', 'Назад в выбор недели', 'Главное меню']))
        except Exception as e:
            print(e)
            temp = change_values[0]
            temp2 = change_values[1]
            change_values.clear()
            change_values.append(temp)
            change_values.append(temp2)
            self.bot.send_message(message.chat.id, "Введите параметр, не стесняйтесь", parse_mode="HTML",
                                  reply_markup=reply_button(['Сохранить', 'Главное меню']))
