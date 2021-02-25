from data_processing import *
from parsing_sheet import update_data, row_index_to_change
from reply_keyboard import Keyboard, get_mark

keyboard = Keyboard


def message_handler(message, bot):
    global keyboard
    keyboard = Keyboard(bot)

    if message.text == 'Показати розклад':
        keyboard.show_schedule(message)

    elif message.text == 'Головне меню':
        send_msg_bot(bot, message)
        clear_user_step("action")

    elif message.text == "Редагувати розклад" or message.text == "Назад в меню редагування розкладу":
        keyboard.edit_schedule(message)
        clear_user_step("action")

    elif message.text == "Редагувати пару" or message.text == "Видалити пару":
        user_step["action"] = message.text
        keyboard.edit_lesson(message)

    elif message.text == "Видалити цю пару":
        keyboard.sure_delete(message)

    elif message.text == "Так":
        for i in range(1, 7):
            update_data(row_index_to_change[int(user_step["lesson_num"]) - 1], i, "")
        keyboard.save_edit_lesson(message)

    elif message.text == "Ні":
        keyboard.save_edit_lesson(message)

    elif message.text == "Парний" or message.text == "Непарний":
        print(status_user("action"))
        if status_user("action"):
            user_step["week"] = message.text
            keyboard.choosing_day(message)
        else:
            send_msg_bot(bot, message)

    elif message.text in days_dict_ua:
        if status_user("week"):
            user_step["day"] = message.text
            keyboard.choosing_lesson(message)
        else:
            send_msg_bot(bot, message)

    elif message.text.isdigit() and message.text in button_list:
        if status_user("day"):
            user_step["lesson_num"] = message.text
            keyboard.choosing_lesson_num(message)
        else:
            send_msg_bot(bot, message)

    elif message.text in items_change_dict:
        if status_user("lesson_num"):
            user_step["item_to_change"] = message.text
            keyboard.choosing_item_to_change(message)
        else:
            send_msg_bot(bot, message)

    elif message.text == "Зберегти":
        if status_user("changed_value"):
            update_data(row_index_to_change[int(user_step["lesson_num"]) - 1],
                        items_change_dict[user_step["item_to_change"]], user_step["changed_value"])
            keyboard.save_edit_lesson(message)
            clear_user_step("item_to_change")
        else:
            send_msg_bot(bot, message)


    # go back buttons

    elif message.text == "Назад до вибору тижня":
        keyboard.edit_lesson(message)
        clear_user_step("week")

    elif message.text == "Назад до вибору дня":
        keyboard.choosing_day(message)
        clear_user_step("day")

    elif status_user("item_to_change"):
        user_step['changed_value'] = message.text
        keyboard.save_changed_value(message)

    print(user_step)


def send_msg_bot(bot, message):
    if message.text == "Головне меню":
        text = message.text
        markup = keyboard.main_menu(True, False)
    elif message.text == "Зберегти":
        text = "Шановний, введіть " + user_step["item_to_change"].lower() + ", а потім тицяйте кнопку!"
        markup = get_mark(True, False)
        markup.add('Зберегти')
        markup.add('Назад до вибору дня', 'Головне меню')
    else:
        markup = keyboard.main_menu(False, False)
        text = "Сталися технічні зміни\nПоверніться до головного меню або перезапустіть бот"
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)
