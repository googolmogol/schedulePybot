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


class Keyboard:

    def __init__(self, bot):
        self.bot = bot

    # just send photo of schedule
    def show_schedule(self, message):
        img = open('restfiles/schedule.jpg', 'rb')
        self.bot.send_photo(message.chat.id, img, "Ваш розклад")

    @staticmethod
    def main_menu(error):
        markup = get_mark(True, False)
        if error:
            markup.add('Показати розклад', 'Редагувати розклад')
        else:
            markup.add('Головне меню')
        return markup

    def edit_schedule(self, message):
        mar = get_mark(True, False)
        mar.add('Додати пару', 'Редагувати пару')
        mar.add('Видалити пару', 'Головне меню')
        self.bot.send_message(message.chat.id, "Оберіть, що необхідно редагувати:", parse_mode="HTML", reply_markup=mar)

    # changing and deleting lesson
    def edit_lesson(self, message):
        markup = get_mark(True, False)
        markup.add('Парний', 'Непарний')
        markup.add('Назад в меню редагування розкладу')
        markup.add('Головне меню')

        self.bot.send_message(message.chat.id, "Оберіть тиждень:", parse_mode="HTML", reply_markup=markup)

    def choosing_day(self, message):
        markup = get_mark(True, True)
        markup.add('Понеділок', 'Вівторок', 'Середа')
        markup.add('Четвер', "П'ятниця", 'Субота')
        markup.add('Неділя')
        markup.add('Назад до вибору тижня', 'Головне меню')

        self.bot.send_message(message.chat.id, 'Оберіть день, коли відбувається пара:', parse_mode="HTML",
                              reply_markup=markup)

    def choosing_lesson(self, message):
        self.bot.send_message(message.chat.id, "Вантажу...почекайте, нічого не клацайте!!!")
        from data_processing import get_lesson_to_change
        from data_processing import user_step

        btn_list, text = get_lesson_to_change(user_step["week"], message.text)
        markup = few_btn_row(btn_list, False)
        self.bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)

    def choosing_lesson_num(self, message):
        from data_processing import get_text_choosing_lesson_num
        text = get_text_choosing_lesson_num(message)
        markup = get_mark(True, False)
        markup.add('Назву пари', 'Викладача', 'Час', 'Посилання', 'Тиждень')
        markup.add('Назад до вибору дня', 'Головне меню')
        self.bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)

    def back_choosing_lesson(self, message):
        markup = get_mark(True, False)
        markup.add('Назву пари', 'Викладача', 'Час', 'Посилання', 'Назад до вибору параметра для редагування',
                   'Головне меню')
        self.bot.send_message(message.chat.id, "Оберіть, що необхідно редагувати:", parse_mode="HTML",
                              reply_markup=markup)


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
