# 1. Подключение нужных модулей
import datetime
import telebot
import tokens
# 2. Создаем бота
bot = telebot.TeleBot(token=tokens.telegram)

# 3. Простой эхо чат
@bot.message_handler(content_types=['text'])
def echo(msg):    
  print(f'[{datetime.datetime.now()}] message: {msg.text}')    
  bot.send_message(chat_id=msg.chat.id, text=msg.text)

# 4. Прослушиваем обновления
if __name__ == '__main__':
    bot.polling(none_stop=True)