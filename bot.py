# 1. Подключение нужных пакетов (батарейки)
from datetime import datetime
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils import logger
from crypto import CoinApi
import ai
import tokens
import requests
from functools import lru_cache

# 2. Создаем бота
bot = TeleBot(token=tokens.telegram)

orders = {}

# 3. Простой эхо чат
# @bot.message_handler(content_types=['text'])
# def echo(msg):
#     print(str(datetime.datetime.now()) + ": " + msg.text)
#     bot.send_message(chat_id=msg.chat.id, text=msg.text)


# 4. Добавляем команды /start
# usage = """*Простой криптобот.*
# Получить текущий курс криптовалют:
#    **/list**, **/coins** - список криптовалют
#    **/rate**, **/price** - текущий курс биткоина в гривне
#    **/rate ETH** - текущий курс эфира в гривне
#    **/rate ETH USD** - текущий курс эфира в долларах США """

base_url = 'http://127.0.0.1:8000/api/'
test_date = datetime(year=2019, month=10, day=21)


@lru_cache(maxsize=None)
@logger
def download_categories():
    response = requests.get(base_url + 'categories/?format=json')
    # print(json.text)
    if response.ok:
        return response.json()
    return []


@lru_cache(maxsize=None)
@logger
def download_menu(day=datetime.now()):
    response = requests.get(
        f'{base_url}days/?format=json&day={day.strftime("%Y-%m-%d")}')
    menu = []
    if response.ok:
        response_json = response.json()
        for dish_url in response_json[0]['dishes']:
            dish = requests.get(dish_url).json()
            dish['category'] = requests.get(dish['category']).json()
            menu.append(dish)
    # print(menu)
    return menu


@logger
def make_order(user, order):
    date = datetime.now()
    json = {
        "date": date.isoformat(),
        "dishes": [f"{base_url}dishes/{d['id']}/" for d in order],
        "client_id": user.id,
        "address": "Телевизионная, 4а"
    }
    print(json)
    response = requests.post(f'{base_url}orders/', json=json)
    return response.json()


usage = """* Добро пожаловать *
Это бот для заказа обедов в оффис.
"""


def category_list(user_id=None):
    markup = InlineKeyboardMarkup(row_width=1)
    for category in download_categories():
        markup.add(InlineKeyboardButton(
            category['name'], callback_data=f"category={category['id']}"))
    if user_id in orders:
        markup.add(InlineKeyboardButton(f'Оформить заказ 💳',
                                        callback_data='order_complete'))
    return markup


@bot.callback_query_handler(func=lambda call: call.data.startswith('order_complete'))
@logger
def callback_order(call):
    user = call.from_user
    if call.message:
        if user.id in orders:
            order = orders.pop(user.id)
            print(order)
            text = "*Ваш заказ:*\n" + \
                "".join(
                    f"- {d['name']} *{d['price']}* грн\n" for d in order)
            price = sum((float(p['price']) for p in order))
            text += f'Общая сумма заказа: *{price}* грн'
            bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
            order_id = make_order(user, order)
            bot.send_message(call.message.chat.id, f"Заказ отрпавлен в обработку. Номер заказа: {order_id['id']}",
                             parse_mode="Markdown")
            bot.send_message(call.message.chat.id,
                             text="Для повторного заказа выполните команду /start")


@bot.message_handler(commands=['start'])
@logger
def start(msg):
    bot.send_message(msg.chat.id, usage, parse_mode="Markdown")
    bot.send_message(msg.chat.id, "Укажите категорию:",
                     reply_markup=category_list())


def dishes_by_category(category_id):
    id = int(category_id)
    category = next(c for c in download_categories() if c['id'] == id)
    dishes = (
        InlineKeyboardButton(
            text=f"{dish['name']} ({dish['weight']}) - {dish['price']} грн",
            callback_data=f"dish={dish['id']}")
        for dish in download_menu(test_date) if dish['category']['id'] == id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*dishes, InlineKeyboardButton(
        text='Вернутся назад ↩', callback_data=f'back'))
    return keyboard, category


@bot.callback_query_handler(func=lambda call: call.data.startswith('category='))
@logger
def callback_category(call):
    if call.message:
        id = call.data.replace('category=', '')
        keyboard, category = dishes_by_category(id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=category['name'], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('back'))
@logger
def callback_back_category(call):
    if call.message:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Укажите категорию:",
                              reply_markup=category_list(call.from_user.id))


@bot.callback_query_handler(func=lambda call: call.data.startswith('dish='))
@logger
def callback_dish(call):
    user = call.from_user
    if call.message:
        id = call.data.replace('dish=', '')
        print('dish id', id)
        dish = next(d for d in download_menu(test_date) if d['id'] == int(id))
        orders.setdefault(user.id, [])
        orders[user.id].append(dish)
        price = sum((float(p['price']) for p in orders[user.id]))
        # {dish['name']} добавлено в меню.
        bot.answer_callback_query(call.id, f"Сумма заказа: {price}")

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
