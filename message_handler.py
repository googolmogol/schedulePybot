from data_processing import *
from reply_keyboard import Keyboard


def message_handler(message, bot):
    keyboard = Keyboard(bot)
    if message.text == 'Показати розклад':
        keyboard.show_schedule(message)

    if message.text == 'Головне меню':
        bot.send_message(message.chat.id, message.text, parse_mode="HTML", reply_markup=keyboard.main_menu(True, False))
        if status_user("Вибрати день"):
            killer_var[0] = True
        clear_user_step("action")

    if message.text == "Редагувати розклад" or message.text == "Назад в меню редагування розкладу":
        killer_var[0] = False
        keyboard.edit_schedule(message)
        clear_user_step("action")

    if message.text == "Редагувати пару" or message.text == "Видалити пару":
        user_step["action"] = message.text
        keyboard.edit_lesson(message)

    if message.text == "Парний" or message.text == "Непарний":
        if status_user("Вибрати дію"):
            user_step["week"] = message.text
            keyboard.choosing_day(message)
        else:
            bot.send_message(message.chat.id, "Сталися технічні зміни\nПоверніться до головного меню або перезапустіть "
                                              "бот", parse_mode="HTML", reply_markup=keyboard.main_menu(False, False))

    if message.text in days_dict_ua:
        killer_var[0] = False
        if status_user("Вибрати тиждень"):
            user_step["day"] = message.text
            keyboard.choosing_lesson(message)
        else:
            bot.send_message(message.chat.id, "Сталися технічні зміни\nПоверніться до головного меню або перезапустіть "
                                              "бот", parse_mode="HTML", reply_markup=keyboard.main_menu(False, False))

    if message.text.isdigit() and message.text in button_list:
        if status_user("Вибрати день"):
            user_step["lesson_num"] = message.text
            keyboard.choosing_lesson_num(message)
        else:
            bot.send_message(message.chat.id, "Сталися технічні зміни\nПоверніться до головного меню або перезапустіть "
                                              "бот", parse_mode="HTML", reply_markup=keyboard.main_menu(False, False))

    # go back buttons

    if message.text == "Назад до вибору тижня":
        keyboard.edit_lesson(message)
        clear_user_step("week")

    if message.text == "Назад до вибору дня":
        keyboard.choosing_day(message)
        clear_user_step("day")

    if user_step["item_to_change"] != '-':
        pass

    print(user_step)

