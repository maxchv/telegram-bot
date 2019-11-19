import datetime
import telebot
import tokens
# 1. Создаем бота
bot = telebot.TeleBot(token=tokens.telegram)

# 2. Создаем клавиатуру


def make_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('1999')
    btn2 = telebot.types.KeyboardButton('1989')
    btn3 = telebot.types.KeyboardButton('2009')
    btn4 = telebot.types.KeyboardButton('2019')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

# 3. команда /start
@bot.message_handler(commands=['start'])
def handler(msg):
    print(f'[{datetime.datetime.now()}] message: {msg.text}')
    bot.send_message(msg.chat.id, "В каком году был создан python?",
                     reply_markup=make_keyboard())

# 4. Обрабатываем ответ
@bot.message_handler(func=lambda msg: True)
def callback(msg):
    year = msg.text
    if year == '1989':
        # Если ответ дан верный, то удаляем клавиатуру
        bot.send_message(msg.chat.id, "Да, это верный ответ",
                         reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))
    else:
        bot.send_message(msg.chat.id, "Увы, но нет")


# 4. Прослушиваем обновления
if __name__ == '__main__':
    bot.polling(none_stop=True)
