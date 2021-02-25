from parsing_sheet import get_lessons_row

user_step = {"action": '-', "week": '-', "day": '-', "lesson_num": '-', "item_to_change": '-'}
items_change_dict = {'Назву пари': 2, 'Викладача': 3, 'Час': 1, 'Посилання': 5, 'Тиждень': 4}
days_dict_ua = {'Понеділок': 1, 'Вівторок': 2, 'Середа': 3, 'Четвер': 4, "П'ятниця": 5, 'Субота': 6, 'Неділя': 7}

button_list = []
lesson_to_change1 = ''


'''class DataProc:

    def __init__(self, bot):
        self.bot = bot
        '''

def get_lesson_to_change(week, day):
    day_digit = days_dict_ua[day]
    button_list.clear()
    text = day + ", пари, " + week.lower() + " тиждень:\n\n"
    global lesson_to_change1
    lesson_to_change1 = get_lessons_row(week.lower(), day_digit)
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


def get_text_choosing_lesson_num(message):
    index = int(message.text)
    text = '\n'
    text += "Пара: " + lesson_to_change1[index - 1][2] + "\nВикладач: " + lesson_to_change1[index - 1][
        3] + "\nЧас: " + lesson_to_change1[index - 1][1] + "\nПосилання: " + '<a href="' + \
        lesson_to_change1[index - 1][5] + '">лінк</a>\nТиждень: ' + lesson_to_change1[index - 1][4]
    text += '\n'
    text += "\nОберіть, що необхідно редагувати:"
    return text
