import telebot

from data_access import *

# dicts instead switch/if-else

# dict of buttons, last value - text to send
button_dict = {
    "Редагувати розклад": ['Додати пару', 'Редагувати пару', 'Видалити пару', 'Головне меню', 'Оберіть дію:'],

    "Назад в редагування розкладу": ['Додати пару', 'Редагувати пару', 'Видалити пару', 'Головне меню', 'Оберіть дію:'],

    "Головне меню": ['Показати розклад', 'Редагувати розклад', 'Головне меню:'],

    "Редагувати пару": ['Парний', 'Непарний', 'Назад в редагування розкладу', 'Оберіть тиждень:'],

    "Удалить пару": ['Парний', 'Непарний', 'Назад в редагування розкладу', 'Оберіть тиждень:'],

    "Назад до вибору тижня": ['Парний', 'Непарний', 'Назад в редагування розкладу', 'Головне меню', 'Оберіть тиждень:'],

    "Парний": ['Понеділок', 'Вівторок', 'Середа', 'Четвер', "П'ятниця", 'Субота', 'Неділя', 'Назад до вибору тижня',
               'Головне меню', 'Оберіть день:'],

    "Непарний": ['Понеділок', 'Вівторок', 'Середа', 'Четвер', "П'ятниця", 'Субота', 'Неділя', 'Назад до вибору тижня',
                 'Головне меню', 'Оберіть день:'],

    "Назад до вибору дня": ['Понеділок', 'Вівторок', 'Середа', 'Четвер', "П'ятниця", 'Субота', 'Неділя',
                            'Назад до вибору тижня', 'Головне меню', 'Оберіть день:'],

    "Назад до вибору параметра для редагування": ['Назву пари', 'Викладача', 'Час', 'Посилання',
                                                  'Оберіть, що необхідно редагувати:'],

}

days_dict_ru = {'Понеділок': 1, 'Вівторок': 2, 'Середа': 3, 'Четвер': 4, "П'ятниця": 5, 'Субота': 6, 'Неділя': 7}

items_change_dict = {'Назву пари': 2, 'Викладача': 3, 'Час': 1, 'Посилання': 5}

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
        self.bot.send_photo(message.chat.id, img, "Ваш розклад")

    # universal fun
    def choose_action(self, message, key):
        global changed_week

        text = button_dict[key][-1]
        button_list = button_dict[key][:-1]
        self.bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=reply_button(button_list))

    # determinate which lessons is on the day
    def day_btn(self, message, day_txt):
        day = days_dict_ru[day_txt]
        print("day in day_btn:", day)
        text = day_txt + ", пари, " + changed_week.lower() + " тиждень:\n\n"
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
        text += "\nОберіть, яку треба редагувати: "
        button_list.append('Назад до вибору дня')
        button_list.append('Головне меню')
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
        text += "\nОберіть, що необхідно редагувати:"
        button_list = ['Назву пари', 'Викладача', 'Час', 'Посилання', 'Назад до вибору параметра для редагування',
                       'Головне меню']
        change_values.append(row_index_to_change[index - 1])  # add row on google sheet of choosen lesson

        self.bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=reply_button(button_list))

    # user choosing data to change
    def change_item(self, message, text):
        change_values.append(items_change_dict[text] + 1)  # add col on google sheet of choosen lesson
        text = 'Введіть ' + text.lower() + ' і натисніть конпку "Зберегти"'
        button_list = ['Зберегти', 'Головне меню']
        self.bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=reply_button(button_list))

    # save changes on google sheet
    def update_entered_data(self, message):
        try:
            update_data(change_values[0], change_values[1], change_values[2])
            print("changed_values in update_entered_data:", change_values)
            temp = change_values[0]
            change_values.clear()
            change_values.append(temp)
            self.bot.send_message(message.chat.id, "Зберіг\nЩо далі, шеф?", parse_mode="HTML", reply_markup=reply_button(
                ['Назад до вибору параметра для редагування', 'Назад до вибору дня', 'Назад до вибору тижня',
                 'Головне меню']))
        except Exception as e:
            print(e)
            temp = change_values[0]
            temp2 = change_values[1]
            change_values.clear()
            change_values.append(temp)
            change_values.append(temp2)
            self.bot.send_message(message.chat.id, "Введіть параметр, не соромтеся", parse_mode="HTML",
                                  reply_markup=reply_button(['Зберегти', 'Головне меню']))
