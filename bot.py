# 1. Подключение нужных пакетов (батарейки)
import datetime
import telebot
from utils import logger
from crypto import CoinApi
import ai
import tokens
import requests

# 2. Создаем бота
bot = telebot.TeleBot(token=tokens.telegram)


# 3. Простой эхо чат
# @bot.message_handler(content_types=['text'])
# def echo(msg):
#     print(str(datetime.datetime.now()) + ": " + msg.text)
#     bot.send_message(chat_id=msg.chat.id, text=msg.text)


# 4. Добавляем команды /start
usage = """*Простой криптобот.*
Получить текущий курс криптовалют:
   **/list**, **/coins** - список криптовалют
   **/rate**, **/price** - текущий курс биткоина в гривне
   **/rate ETH** - текущий курс эфира в гривне
   **/rate ETH USD** - текущий курс эфира в долларах США """

response = requests.get('http://127.0.0.1:8000/api/categories/?format=json')
# print(json.text)
categories = response.json()

response = requests.get(
    'http://127.0.0.1:8000/api/days/?format=json&day=2019-10-21')
response_json = response.json()
menu = []
for dish_url in response_json[0]['dishes']:
    dish = requests.get(dish_url).json()
    dish['category'] = requests.get(dish['category']).json()
    menu.append(dish)
print(menu)


@bot.message_handler(commands=['start'])
@logger
def start(msg):
    # bot.send_message(msg.chat.id, usage, parse_mode="Markdown")
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for category in categories:
        markup.add(telebot.types.InlineKeyboardButton(
            category['name'], callback_data=f"category={category['id']}"))
    bot.send_message(msg.chat.id, "Укажите категорию:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('category='))
@logger
def callback_category(call):
    if call.message:
        id = call.data.replace('category=', '')
        category = next(c for c in categories if c['id'] == int(id))
        dishes = (
            telebot.types.InlineKeyboardButton(
                text=f"{dish['name']} ({dish['weight']}) - {dish['price']} грн", callback_data=f"dish={dish['id']}")
            for dish in menu if dish['category']['id'] == int(id))
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*dishes, telebot.types.InlineKeyboardButton(
            text='Вернутся назад', callback_data=f'back=category:{id}'))
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=category['name'], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('back='))
@logger
def callback_back_category(call):
    if call.message:
        pass


@bot.callback_query_handler(func=lambda call: call.data.startswith('dish='))
@logger
def callback_dish(call):
    if call.message:
        id = call.data.replace('dish=', '')
        dish = next(d for d in menu if d['id'] == int(id))
        bot.answer_callback_query(call.id, f"{dish['name']} добавлено в меню")
        print('dish id', id)

# @bot.message_handler(commands=['start'])
# @logger
# def start(msg):
#     bot.send_message(msg.chat.id, usage, parse_mode="Markdown")


# # 5. Команды /rate /price
# @bot.message_handler(commands=['rate', 'price'])
# @logger
# def crypto_rates(msg):
#     args = msg.text.split()
#     crypto = 'BTC'
#     currency = 'UAH'
#     if len(args) > 2:
#         crypto = args[1]
#         currency = args[2]
#     elif len(args) == 2:
#         crypto = args[1]
#     print(crypto, currency)
#     coin = CoinApi(crypto=crypto.upper(), currency=currency.upper())
#     text = 'Курс для {}: {} {}'.format(coin.crypto, coin.get(), coin.currency)
#     bot.send_message(msg.chat.id, text)


# # 6. Команды /list /coins
# @bot.message_handler(commands=['list', 'coins'])
# @logger
# def list_currencies(msg):
#     text = "Список поддерживаемых криптовалют: {}".format(
#         ', '.join(CoinApi.coins))
#     bot.send_message(msg.chat.id, text)


# # 7. Немного AI
# @bot.message_handler(content_types=['text'])
# @logger
# def textMessage(msg):
#     bot.send_message(chat_id=msg.chat.id, text=ai.smallTalk(msg.text))


if __name__ == '__main__':
    print('Started')
    bot.polling(none_stop=True)
    print('End')
