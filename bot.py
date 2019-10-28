# 1. Подключение нужных пакетов (батарейки)
from telebot import TeleBot
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, User, LabeledPrice
import tokens
import logging
from utils import logger
from rest import Service
from context import Context

# 2. Создаем бота
bot = TeleBot(token=tokens.telegram)

log = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.

usage = """* Добро пожаловать *
Это бот для заказа обедов в офис.
"""


class Register(object):

    def __init__(self):
        self.__register = {}

    @logger
    def start(self, user: User):
        if user.id not in self.__register:
            ctx = Context(user)
            self.__register[user.id] = ctx

    def context(self, user: User) -> Context:
        return next((self.__register.get(ctx) for ctx in self.__register if ctx == user.id))

    def set_address(self, user: User, address: str):
        ctx = self.context(user)
        ctx.address = address

    def exists(self, user: User):
        return user.id in self.__register

    def add_dish(self, user: User, dish: dict):
        ctx = self.context(user)
        ctx.add_dish(dish)

    def back(self, user: User):
        ctx = self.context(user)

    def price(self, user: User) -> float:
        ctx = self.context(user)
        return ctx.price

    def pop(self, user_id: int) -> Context:
        return self.__register.pop(user_id)


register = Register()
rest = Service()


def category_list(user: User = None):
    markup = InlineKeyboardMarkup(row_width=1)
    for category in rest.categories:
        markup.add(InlineKeyboardButton(
            category['name'], callback_data=f"category={category['id']}"))

    if user:
        ctx = register.context(user)
        if len(ctx.dishes):
            markup.add(InlineKeyboardButton(f'Оформить заказ 💳',
                                            callback_data='set_address'))
    return markup


@bot.message_handler(commands=['start'])
@logger
def start(msg: Message):
    '''
    First step: /start command.
    Choose category
    '''
    register.start(msg.from_user)
    bot.send_message(msg.chat.id, usage, parse_mode="Markdown")
    bot.send_message(msg.chat.id, "Укажите категорию:",
                     reply_markup=category_list())


def dishes_by_category(category_id):
    id = int(category_id)
    category = next(c for c in rest.categories if c['id'] == id)
    dishes = (
        InlineKeyboardButton(
            text=f"{dish['name']} ({dish['weight']}) - {dish['price']} грн",
            callback_data=f"dish={dish['id']}")
        for dish in rest.menu if dish['category']['id'] == id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*dishes, InlineKeyboardButton(
        text='« Вернутся назад', callback_data=f'back'))
    return keyboard, category


@bot.callback_query_handler(func=lambda call: call.data.startswith('category='))
@logger
def callback_category(call: CallbackQuery):
    '''
    Second step choose dishes
    '''
    if call.message:
        id = call.data.replace('category=', '')
        keyboard, category = dishes_by_category(id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=category['name'], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('dish='))
@logger
def callback_dish(call: CallbackQuery):
    '''
    Third step: add dish to basket
    '''
    user = call.from_user
    if call.message:
        id = call.data.replace('dish=', '')
        dish = next(d for d in rest.menu if d['id'] == int(id))
        register.add_dish(user, dish)
        price = register.context(user).price
        # {dish['name']} добавлено в меню.
        bot.answer_callback_query(call.id, f"Сумма заказа: {price}")


@bot.callback_query_handler(func=lambda call: call.data == 'back')
@logger
def callback_back_category(call: CallbackQuery):
    '''
    Fourth step: go back to category
    '''
    if call.message:
        register.back(call.from_user)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Укажите категорию:",
                              reply_markup=category_list(call.from_user))


def order_complete_handler(msg: Message):
    if msg:
        user = msg.from_user
        register.set_address(user, msg.text)
        if register.exists(user):
            ctx = register.context(user)
            text = "Ваш заказ:\n" + \
                "".join(
                    f"- {d['name']} {d['price']} грн\n" for d in ctx.dishes)
            text += f'Общая сумма заказа: {ctx.price} грн'
            #bot.send_message(msg.chat.id, text, parse_mode="Markdown")
            prices = [LabeledPrice(label=d['name'], amount=int(
                float(d['price']) * 100)) for d in ctx.dishes]
            bot.send_invoice(msg.chat.id,
                             title='Обеды в офис',
                             description=text,
                             provider_token=tokens.liqPay,
                             currency='uah',
                             prices=prices,
                             start_parameter='office-lunch',
                             invoice_payload='LUNCH')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(msg: Message):
    ctx = register.pop(msg.from_user.id)
    order_id = rest.make_order(ctx)
    bot.send_message(msg.chat.id, f"Заказ отрпавлен в обработку. Номер заказа: {order_id['id']}",
                     parse_mode="Markdown")
    bot.send_message(msg.chat.id,
                     text="Для нового заказа выполните команду /start")


@bot.callback_query_handler(func=lambda call: call.data == 'set_address')
@logger
def callback_order(call: CallbackQuery):
    bot.register_next_step_handler(call.message, order_complete_handler)
    bot.send_message(call.message.chat.id, "Введите адрес доставки")


if __name__ == '__main__':
    print('Started')
    bot.polling(none_stop=True)
    print('End')
