import telebot


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
        self.bot.send_photo(message.chat.id, img, "<strong>Ваш розклад</strong>", parse_mode="HTML")

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
        text = "<strong>Оберіть, що необхідно редагувати:</strong>"
        self.send_msg_to_bot(message, text, mar)

    # changing and deleting lesson
    def edit_lesson(self, message):
        markup = get_mark(True, False)
        markup.add('Парний', 'Непарний', 'Обидва')
        markup.add('Назад в меню редагування розкладу', 'Головне меню')

        text = "<strong>Оберіть тиждень:</strong>"
        self.send_msg_to_bot(message, text, markup)

    def choosing_day(self, message):
        markup = get_mark(True, True)
        markup.add('Понеділок', 'Вівторок', 'Середа')
        markup.add('Четвер', "П'ятниця", 'Субота')
        markup.add('Неділя')
        from data_processing import status_user
        from data_processing import user_step_add
        if status_user(user_step_add, "action"):
            text = '<strong>Оберіть день, на який необхідно додати пару:</strong>'
            markup.add('Назад в меню редагування розкладу', 'Головне меню')
        else:
            text = '<strong>Оберіть день, коли відбувається пара:</strong>'
            markup.add('Назад до вибору тижня', 'Головне меню')

        self.send_msg_to_bot(message, text, markup)

    def choosing_lesson(self, message):
        self.bot.send_message(message.chat.id, "<strong>Вантажу...почекайте, нічого не клацайте!!!</strong>",
                              parse_mode="HTML")
        from data_processing import get_lesson_to_change
        from data_processing import user_step_edit

        btn_list, text = get_lesson_to_change(user_step_edit["week"], message.text)
        markup = few_btn_row(btn_list, False)
        self.send_msg_to_bot(message, text, markup)

    def choosing_lesson_num(self, message):
        from data_processing import get_text_choosing_lesson_num
        text = get_text_choosing_lesson_num(message)
        markup = get_mark(True, False)
        from data_processing import user_step_edit
        if user_step_edit['action'] == 'Редагувати пару':
            markup.add('Назву пари', 'Викладача', 'Час', 'Посилання', 'Тиждень')
            markup.add('Назад до вибору дня', 'Головне меню')
        if user_step_edit['action'] == 'Видалити пару':
            markup.add('Видалити цю пару')
            markup.add('Назад до вибору дня', 'Головне меню')
        self.send_msg_to_bot(message, text, markup)

    def back_choosing_lesson(self, message):
        markup = get_mark(True, False)
        markup.add('Назву пари', 'Викладача', 'Час', 'Посилання', 'Назад до вибору параметра для редагування',
                   'Головне меню')
        text = "<strong>Оберіть, що необхідно редагувати:</strong>"
        self.send_msg_to_bot(message, text, markup)

    def choosing_item_to_change(self, message):
        markup = get_mark(True, False)
        markup.add('Зберегти')
        markup.add('Назад до вибору дня', 'Головне меню')
        from data_processing import user_step_edit
        text = "<strong>Введіть " + user_step_edit["item_to_change"].lower() + \
               ' та натисність кнопку "Зберегти"</strong>'
        self.send_msg_to_bot(message, text, markup)

    def enter_lesson_values(self, message, text, last):
        if last:
            markup = get_mark(True, False)
            markup.add('Зберегти додану пару')
            markup.add('Назад в меню редагування', 'Головне меню')
            self.send_msg_to_bot(message, text, markup)
        else:
            self.bot.send_message(message.chat.id, text, parse_mode="HTML")

    def save_changed_value(self, message):
        markup = get_mark(True, False)
        markup.add('Зберегти', 'Назад до вибору дня')
        text = '<strong>Натисність кнопку "Зберегти"</strong>'
        self.send_msg_to_bot(message, text, markup)

    def save_edit_lesson(self, message):
        markup = get_mark(True, False)
        markup.add('Назад до вибору дня', 'Головне меню')
        from data_processing import user_step_edit
        text = "<strong>Зберіг\nЩо далі, шеф?</strong>"

        if message.text == "Так" and user_step_edit["action"] == 'Видалити пару':
            text = "<strong>Видалив\nСподіваюсь, що пари дійсно немає</strong>"

        elif message.text == "Ні" and user_step_edit["action"] == 'Видалити пару':
            text = "<strong>Охрана атмєна</strong>"
        self.send_msg_to_bot(message, text, markup)

    def sure_delete(self, message):
        markup = get_mark(True, False)
        markup.add('Так', 'Ні')
        from data_processing import lesson_to_change1
        from data_processing import user_step_edit
        text = 'Ви впевнені, що хочете видалити пару "' + lesson_to_change1[int(user_step_edit['lesson_num']) - 1][2] + \
               '"?'
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


