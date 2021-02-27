from data_processing import *
from parsing_sheet import update_data, row_index_to_change, add_new_lesson, days_dict
from reply_keyboard import Keyboard, get_mark

keyboard = Keyboard

main_menu_list = ['Показати розклад', 'Головне меню', 'Редагувати розклад', 'Назад в меню редагування розкладу']
edit_schedule_list = ['Редагувати пару', 'Видалити пару', 'Парний', 'Непарний', 'Обидва', 'Зберегти',
                      'Видалити цю пару',
                      'Зберегти додану пару', 'Так', 'Ні', 'Додати пару']

back_buttons_list = ['Назад до вибору тижня', 'Назад до вибору дня']


def message_handler(message, bot):
    global keyboard
    keyboard = Keyboard(bot)

    try:

        ###################
        # MAIN MENU #######
        ###################
        if message.text in main_menu_list:

            if message.text == 'Показати розклад':
                keyboard.show_schedule(message)

            elif message.text == 'Головне меню':
                send_msg_bot(bot, message)
                clear_user_step(user_step_edit, "action")
                clear_user_step(user_step_add, "action")

            elif message.text == "Редагувати розклад" or message.text == "Назад в меню редагування розкладу":
                keyboard.edit_schedule(message)
                clear_user_step(user_step_edit, "action")
                clear_user_step(user_step_add, "action")

        ###################
        # EDIT SCHEDULE ###
        ###################
        elif message.text in edit_schedule_list:

            if message.text == "Редагувати пару" or message.text == "Видалити пару":
                user_step_edit["action"] = message.text
                keyboard.edit_lesson(message)

            elif message.text == "Додати пару":
                user_step_add["action"] = message.text
                keyboard.choosing_day(message)

            elif message.text == "Парний" or message.text == "Непарний" or message.text == "Обидва":
                if status_user(user_step_edit, "action"):
                    user_step_edit["week"] = message.text
                    keyboard.choosing_day(message)
                elif status_user(user_step_add, "teacher"):
                    user_step_add["week"] = message.text.lower()
                    text = "<strong>Введіть лінк:</strong>"
                    keyboard.enter_lesson_values(message, text, False)
                else:
                    send_msg_bot(bot, message)

            elif message.text == "Зберегти":
                if status_user(user_step_edit, "changed_value"):
                    update_data(row_index_to_change[int(user_step_edit["lesson_num"]) - 1],
                                items_change_dict[user_step_edit["item_to_change"]], user_step_edit["changed_value"])
                    keyboard.save_edit_lesson(message)
                    clear_user_step(user_step_edit, "item_to_change")
                else:
                    send_msg_bot(bot, message)

            elif message.text == "Зберегти додану пару":
                if status_user(user_step_add, "link"):
                    add_new_lesson(list(user_step_add.values())[1:])
                    send_msg_bot(bot, message)
                    clear_user_step(user_step_add, "action")
                else:
                    send_msg_bot(bot, message)

            elif message.text == "Видалити цю пару":
                if status_user(user_step_edit, "lesson_num"):
                    keyboard.sure_delete(message)

            elif message.text == "Так":
                for i in range(1, 7):
                    update_data(row_index_to_change[int(user_step_edit["lesson_num"]) - 1], i, "")
                keyboard.save_edit_lesson(message)

            elif message.text == "Ні":
                keyboard.save_edit_lesson(message)

        ###################
        # DAYS CHOOSING ###
        ###################
        elif message.text in days_dict_ua:
            if status_user(user_step_edit, "week"):
                user_step_edit["day"] = message.text
                keyboard.choosing_lesson(message)
            elif status_user(user_step_add, "action"):
                user_step_add["day"] = days_dict[days_dict_ua[message.text]]
                text = '<strong>Введіть час пари, наприклад: "13:15":</strong>'
                keyboard.enter_lesson_values(message, text, False)
            else:
                send_msg_bot(bot, message)

        ###################
        # LESSON NUMBER ###
        ###################
        elif message.text.isdigit() and message.text in button_list:
            if status_user(user_step_edit, "day"):
                user_step_edit["lesson_num"] = message.text
                keyboard.choosing_lesson_num(message)
            else:
                send_msg_bot(bot, message)

        ###################
        # ITEMS TO CHANGE #
        ###################
        elif message.text in items_change_dict:
            if status_user(user_step_edit, "lesson_num"):
                user_step_edit["item_to_change"] = message.text
                keyboard.choosing_item_to_change(message)
            else:
                send_msg_bot(bot, message)

        ###################
        # BACK BUTTONS  ###
        ###################
        elif message.text == "Назад до вибору тижня":
            keyboard.edit_lesson(message)
            clear_user_step(user_step_edit, "week")

        elif message.text == "Назад до вибору дня":
            keyboard.choosing_day(message)
            clear_user_step(user_step_edit, "day")

        ########################################
        # DEFINE USER STATUS TO ADD NEW LESSON #
        ########################################

        elif status_user(user_step_edit, "item_to_change"):

            if user_step_edit["item_to_change"] == "Час":
                if datetime_format(message.text)[1]:
                    user_step_edit['changed_value'] = datetime_format(message.text)[0]
                    keyboard.save_changed_value(message)
                else:
                    bot.send_message(message.chat.id, datetime_format(message.text)[0])
            else:
                user_step_edit['changed_value'] = message.text
                keyboard.save_changed_value(message)

        elif status_user(user_step_add, "week"):
            user_step_add["link"] = message.text
            text = '<strong>Натисніть кнопку "Зберегти додану пару" для додавання пари:</strong>'
            keyboard.enter_lesson_values(message, text, True)

        elif status_user(user_step_add, "lesson_name"):
            user_step_add["teacher"] = message.text
            keyboard.edit_lesson(message)

        elif status_user(user_step_add, "time"):
            user_step_add["lesson_name"] = message.text
            text = "<strong>Введіть вчителя:</strong>"
            keyboard.enter_lesson_values(message, text, False)

        elif status_user(user_step_add, "day"):
            if datetime_format(message.text)[1]:
                user_step_add["time"] = datetime_format(message.text)[0]
                text = "<strong>Введіть назву пари:</strong>"
            else:
                text = datetime_format(message.text)[0]
            keyboard.enter_lesson_values(message, text, False)

        else:
            send_msg_bot(bot, message)

        print('edit:', user_step_edit)
        print('add:', user_step_add)

    except Exception as e:
        print(e)
        send_msg_bot(bot, message)

def send_msg_bot(bot, message):
    if message.text == "Головне меню":
        text = message.text
        markup = keyboard.main_menu(True, False)
    elif message.text == "Зберегти":
        text = "Шановний, введіть " + user_step_edit["item_to_change"].lower() + ", а потім тицяйте кнопку!"
        markup = get_mark(True, False)
        markup.add('Зберегти')
        markup.add('Назад до вибору дня', 'Головне меню')
    elif message.text == "Зберегти додану пару":
        markup = get_mark(True, False)
        markup.add('Головне меню')
        text = "<strong>Зберіг\nЩо далі, шеф?</strong>"
    else:
        markup = keyboard.main_menu(False, False)
        text = "Сталися технічні зміни\nПоверніться до головного меню або перезапустіть бот"

    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)
