# 1. Подключение нужных пакетов (батарейки)
import datetime
import telebot
from utils import logger
from crypto import CoinApi
import ai
import tokens

# 2. Создаем бота
bot = telebot.TeleBot(token=tokens.telegram)


# 3. Простой эхо чат
# @bot.message_handler(content_types=['text'])
def echo(msg):
    print(str(datetime.datetime.now()) + ": " + msg.text)
    bot.send_message(chat_id=msg.chat.id, text=msg.text)


# 4. Добавляем команды /start
usage = """*Простой криптобот.*
Получить текущий курс криптовалют:
   **/list**, **/coins** - список криптовалют 
   **/rate**, **/price** - текущий курс биткоина в гривне 
   **/rate ETH** - текущий курс эфира в гривне 
   **/rate ETH USD** - текущий курс эфира в долларах США """


@bot.message_handler(commands=['start'])
@logger
def start(msg):
    bot.send_message(msg.chat.id, usage, parse_mode="Markdown")


# 5. Команды /rate /price
@bot.message_handler(commands=['rate', 'price'])
@logger
def crypto_rates(msg):
    args = msg.text.split()
    crypto = 'BTC'
    currency = 'UAH'
    if len(args) > 2:
        crypto = args[1]
        currency = args[2]
    elif len(args) == 2:
        crypto = args[1]
    print(crypto, currency)
    coin = CoinApi(crypto=crypto.upper(), currency=currency.upper())
    text = 'Курс для {}: {} {}'.format(coin.crypto, coin.get(), coin.currency)
    bot.send_message(msg.chat.id, text)


# 6. Команды /list /coins
@bot.message_handler(commands=['list', 'coins'])
@logger
def list_currencies(msg):
    text = "Список поддерживаемых криптовалют: {}".format(', '.join(CoinApi.coins))
    bot.send_message(msg.chat.id, text)


# 7. Немного AI
@bot.message_handler(content_types=['text'])
@logger
def textMessage(msg):
    bot.send_message(chat_id=msg.chat.id, text=ai.smallTalk(msg.text))


if __name__ == '__main__':
    bot.polling(none_stop=True)
