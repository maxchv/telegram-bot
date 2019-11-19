import datetime
import telebot
import tokens
# 1. Создаем бота
bot = telebot.TeleBot(token=tokens.telegram)

# 2. Создаем клавиатуру
def make_keyboard():
  markup = telebot.types.InlineKeyboardMarkup(row_width=2)
  btn1 = telebot.types.InlineKeyboardButton('1999', callback_data='year:1999')
  btn2 = telebot.types.InlineKeyboardButton('1989', callback_data='year:1989')
  btn3 = telebot.types.InlineKeyboardButton('2009', callback_data='year:2009')
  btn4 = telebot.types.InlineKeyboardButton('2019', callback_data='year:2019')
  markup.add(btn1, btn2, btn3, btn4)
  return markup

# 3. команда /start
@bot.message_handler(commands=['start'])
def handler(msg):
  print(f'[{datetime.datetime.now()}] message: {msg.text}')   
  bot.send_message(msg.chat.id, "В каком году был создан python?", reply_markup=make_keyboard())

# 4. Обрабатываем ответ
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    text, year = call.data.split(":")
    if year == '1989':
      bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Да, в ' + year)
    else:
      bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=year+'?', 
                              reply_markup=make_keyboard())


# 4. Прослушиваем обновления
if __name__ == '__main__':
    bot.polling(none_stop=True)