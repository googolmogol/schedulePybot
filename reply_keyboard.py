import telebot

# dicts instead switch/if-else

# dict of buttons, last value - text to send

# list which holds values to change:
# [0] - row
# [1] - col
# [2] - value to change

change_values = []

changed_week = ''  # var to define which week choose user


def get_mark(resize, onetime):
    return telebot.types.ReplyKeyboardMarkup(resize, onetime)


# creating inline buttons
def inline_button(text, url):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text=text, url=url)
    markup.add(button)
    return markup


class Keyboard:

    def __init__(self, bot):
        self.bot = bot

    # just send photo of schedule
    def show_schedule(self, message):
        img = open('restfiles/schedule.jpg', 'rb')
        self.bot.send_photo(message.chat.id, img, "Ваш розклад")

    def send_msg_to_bot(self, message, text, markup):
        self.bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)

    @staticmethod
    def main_menu(error, hide):
        markup = get_mark(True, hide)
        if error:
            markup.add('Показати розклад', 'Редагувати розклад')
        else:
            markup.add('Головне меню')
        return markup

    def edit_schedule(self, message):
        mar = get_mark(True, False)
        mar.add('Додати пару', 'Редагувати пару')
        mar.add('Видалити пару', 'Головне меню')
        text = "Оберіть, що необхідно редагувати:"
        self.send_msg_to_bot(message, text, mar)

    # changing and deleting lesson
    def edit_lesson(self, message):
        markup = get_mark(True, False)
        markup.add('Парний', 'Непарний')
        markup.add('Назад в меню редагування розкладу')
        markup.add('Головне меню')
        text = "Оберіть тиждень:"
        self.send_msg_to_bot(message, text, markup)

    def choosing_day(self, message):
        markup = get_mark(True, True)
        markup.add('Понеділок', 'Вівторок', 'Середа')
        markup.add('Четвер', "П'ятниця", 'Субота')
        markup.add('Неділя')
        markup.add('Назад до вибору тижня', 'Головне меню')
        text = 'Оберіть день, коли відбувається пара:'
        self.send_msg_to_bot(message, text, markup)

    def choosing_lesson(self, message):
        self.bot.send_message(message.chat.id, "Вантажу...почекайте, нічого не клацайте!!!")
        from data_processing import get_lesson_to_change
        from data_processing import user_step

        btn_list, text = get_lesson_to_change(user_step["week"], message.text)
        markup = few_btn_row(btn_list, False)
        self.send_msg_to_bot(message, text, markup)

    def choosing_lesson_num(self, message):
        from data_processing import get_text_choosing_lesson_num
        text = get_text_choosing_lesson_num(message)
        markup = get_mark(True, False)
        from data_processing import user_step
        if user_step['action'] == 'Редагувати пару':
            markup.add('Назву пари', 'Викладача', 'Час', 'Посилання', 'Тиждень')
            markup.add('Назад до вибору дня', 'Головне меню')
        if user_step['action'] == 'Видалити пару':
            markup.add('Видалити цю пару')
            markup.add('Назад до вибору дня', 'Головне меню')
        self.send_msg_to_bot(message, text, markup)

    def back_choosing_lesson(self, message):
        markup = get_mark(True, False)
        markup.add('Назву пари', 'Викладача', 'Час', 'Посилання', 'Назад до вибору параметра для редагування',
                   'Головне меню')
        text = "Оберіть, що необхідно редагувати:"
        self.send_msg_to_bot(message, text, markup)

    def choosing_item_to_change(self, message):
        markup = get_mark(True, False)
        markup.add('Зберегти')
        markup.add('Назад до вибору дня', 'Головне меню')
        from data_processing import user_step
        text = "Введіть " + user_step["item_to_change"].lower() + ' та натисність кнопку "Зберегти"'
        self.send_msg_to_bot(message, text, markup)

    def save_changed_value(self, message):
        markup = get_mark(True, False)
        markup.add('Зберегти', 'Назад до вибору дня')
        text = 'Натисність кнопку "Зберегти"'
        self.send_msg_to_bot(message, text, markup)

    def save_edit_lesson(self, message):
        markup = get_mark(True, False)
        markup.add('Назад до вибору дня', 'Головне меню')
        from data_processing import user_step
        text = "Зберіг\nЩо далі, шеф?"

        if message.text == "Так" and user_step["action"] == 'Видалити пару':
            text = "Видалив\nСподіваюсь, що пари дійсно немає"

        elif message.text == "Ні" and user_step["action"] == 'Видалити пару':
            text = "Охрана атмєна"
        self.send_msg_to_bot(message, text, markup)

    def sure_delete(self, message):
        markup = get_mark(True, False)
        markup.add('Так', 'Ні')
        from data_processing import lesson_to_change1
        from data_processing import user_step
        print(lesson_to_change1[0][1])
        text = 'Ви впевнені, що хочете видалити пару "' + lesson_to_change1[int(user_step['lesson_num']) - 1][2] + '"?'
        self.send_msg_to_bot(message, text, markup)


# function which creates few reply buttons in the row
def few_btn_row(btn_list, hide):
    markup = get_mark(True, hide)
    length = len(btn_list) - 2
    if length >= 3:
        length2 = length % 3
        if length2 == 0:
            for i in range(0, length, 3):
                markup.add(btn_list[i], btn_list[i+1], btn_list[i+2])
        elif length2 == 1:
            for i in range(0, length - 1, 3):
                markup.add(btn_list[i], btn_list[i+1], btn_list[i+2])
            markup.add(btn_list[length - 1])
        elif length2 == 2:
            for i in range(0, length - 2, 3):
                markup.add(btn_list[i], btn_list[i+1], btn_list[i+2])
            markup.add(btn_list[length-2], btn_list[length-1])
    elif length == 2:
        markup.add(btn_list[0], btn_list[1])
    elif length == 1:
        markup.add(btn_list[0])
    markup.add(btn_list[-2], btn_list[-1])
    return markup
