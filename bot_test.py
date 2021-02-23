import telebot

bot = telebot.TeleBot("801359509:AAHjuBl_1xRdDHHTTacpT3Q1TSiXl_qQiCw")


@bot.message_handler(commands=['start'])
def handle_text(message):
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.row('Показать расписание')
    markup.row('Изменить расписание')

    bot.send_message(message.chat.id, '<strong>Здарова студентам!</strong>\N{Victory Hand}\nЯ бот, который будет '
                                      'уведомлять о парах \N{Robot Face}\n ', parse_mode="HTML", reply_markup=markup)


@bot.message_handler(func=lambda mess: "Показать расписание" == mess.text, content_types=['text'])
def handle_text(message):
    img = open('restfiles/schedule.jpg', 'rb')
    bot.send_photo(message.chat.id, img, "Ваше расписание")

bot.polling(none_stop=True)
