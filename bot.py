# 1. Подключение нужных пакетов (батарейки)
from datetime import datetime
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, User
from utils import logger
import tokens
import requests
from functools import lru_cache
from enum import Enum

# 2. Создаем бота
bot = TeleBot(token=tokens.telegram)


class Status(Enum):
    UNKNOWN = 'unknown'
    START = 'start'
    CHOOSE_DISH = 'choose dish'


class Event(Enum):
    CREATED = 'created'
    BACK = 'back'
    CHOOSE_CATEGORY = 'choose category'
    COOSE_DISH = 'choose dish'
    SET_STATUS = 'set status'

class Context:

    def __init__(self):
        self.__status = Status.UNKNOWN
        self.__dishes = []
        self.__category = None
        self.__history = [{'timestamp': datetime.now(), 'event': Event.CREATED}]

    def __save(self, status: Status, args: any = None):
        self.__history.append({'timestamp': datetime.now(), 'event': Status, 'args': args})

    def add_dish(self, dish):
        self.__save(Event.COOSE_DISH, dish)
        self.dishes.append(dish)

    @property
    def dishes(self):
        return self.__dishes

    @property
    def category(self) -> int:
        return self.__category

    @category.setter
    def category(self, value: int):
        self.__save(Event.CHOOSE_CATEGORY, value)
        self.__category = value

    @properyt
    def status(self) -> Status:
        return self.__status

    @status.setter
    def status(self, value: Status):
        self.__save(status)
        self.__status = value

orders = {}
statuses = {}


class Order:

    def set_status(self, user: User, status: Status):
        statuses.setdefault(user.id, {})
        statuses[user.id]['status'] = status
        pass

    def get_status(self, user: User):
        return statuses[user.id]['status'] if user.id in statuses else Status.UNKNOWN


order = Order()

# 3. Простой эхо чат
# @bot.message_handler(content_types=['text'])
# def echo(msg):
#     print(str(datetime.datetime.now()) + ": " + msg.text)
#     bot.send_message(chat_id=msg.chat.id, text=msg.text)


# 4. Добавляем команды /start

# @bot.message_handler(commands=['start'])
# @logger
# def start(msg):
#     bot.send_message(msg.chat.id, usage, parse_mode="Markdown")

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
    response = requests.post(f'{base_url}orders/', json=json)
    return response.json()


usage = """* Добро пожаловать *
Это бот для заказа обедов в офис.
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
def callback_order(call: CallbackQuery):
    user = call.from_user
    if call.message:
        if user.id in orders:
            order = orders.pop(user.id)
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
def start(msg: Message):
    user = msg.from_user
    order.set_status(user, Status.START)
    print(user)
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
        text='« Вернутся назад', callback_data=f'back'))
    return keyboard, category


# @bot.callback_query_handler(func=lambda call: call.data.startswith('category='))
@bot.callback_query_handler(func=lambda call: order.get_status(call.from_user) == Status.START and call.data.startswith('category='))
@logger
def callback_category(call: CallbackQuery):
    if call.message:
        order.set_status(call.from_user, Status.CHOOSE_DISH)
        id = call.data.replace('category=', '')
        keyboard, category = dishes_by_category(id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=category['name'], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('back'))
@logger
def callback_back_category(call: CallbackQuery):
    if call.message:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Укажите категорию:",
                              reply_markup=category_list(call.from_user.id))


@bot.callback_query_handler(func=lambda call: call.data.startswith('dish='))
@logger
def callback_dish(call: CallbackQuery):
    user = call.from_user
    if call.message:
        id = call.data.replace('dish=', '')
        dish = next(d for d in download_menu(test_date) if d['id'] == int(id))
        orders.setdefault(user.id, [])
        orders[user.id].append(dish)
        price = sum((float(p['price']) for p in orders[user.id]))
        # {dish['name']} добавлено в меню.
        bot.answer_callback_query(call.id, f"Сумма заказа: {price}")


# # 5. Команды /rate /price


# # 6. Команды /list /coins


# # 7. Немного AI
# @bot.message_handler(content_types=['text'])
# @logger
# def textMessage(msg):
#     bot.send_message(chat_id=msg.chat.id, text=ai.smallTalk(msg.text))


if __name__ == '__main__':
    print('Started')
    bot.polling(none_stop=True)
    print('End')
