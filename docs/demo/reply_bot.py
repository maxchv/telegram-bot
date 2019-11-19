import datetime
import telebot
import tokens
# 2. Создаем бота
bot = telebot.TeleBot(token=tokens.telegram)

# 3. метод reply_to позволяет добавить ответ на запрос
@bot.message_handler(func=lambda m: True)
def handler(msg):
    print(f'[{datetime.datetime.now()}] message: {msg.text}')
    bot.reply_to(message=msg, text="Ответ на запрос")


# 4. Прослушиваем обновления
if __name__ == '__main__':
    bot.polling(none_stop=True)
