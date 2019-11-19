import datetime
import telebot
import tokens
# 2. Создаем бота
bot = telebot.TeleBot(token=tokens.telegram)

# 3. Обрабатываем комманды https://tlgrm.ru/docs/bots#commands
# Команда /start
@bot.message_handler(commands=['start'])
def start_handler(msg):
  print(f'[{datetime.datetime.now()}] message: {msg.text}')   
  bot.send_message(chat_id=msg.chat.id, text="Добро пожаловать")

# Команда /help
@bot.message_handler(commands=['help'])
def help_handler(msg):   
  print(f'[{datetime.datetime.now()}] message: {msg.text}')
  bot.send_message(chat_id=msg.chat.id, text="Это справка")

# Команда /settings
@bot.message_handler(commands=['settings'])
def help_handler(msg):   
  print(f'[{datetime.datetime.now()}] message: {msg.text}')
  bot.send_message(chat_id=msg.chat.id, text="Это настройки")

# 4. Прослушиваем обновления
if __name__ == '__main__':
    bot.polling(none_stop=True)