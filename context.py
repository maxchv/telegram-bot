from datetime import datetime
from enum import Enum
from telebot.types import User


class Event(Enum):
    CREATED = 'created'
    BACK = 'back'
    CHOOSE_CATEGORY = 'choose category'
    COOSE_DISH = 'choose dish'
    SET_STATUS = 'set status'


class Context:

    def __init__(self, user: User):
        self.__user = user
        self.__address = ''
        self.__dishes = []
        self.__history = [
            {'timestamp': datetime.now(), 'event': Event.CREATED}]

    def __save(self, event: Event, args: any = None):
        self.__history.append(
            {'timestamp': datetime.now(), 'event': event, 'args': args})

    def add_dish(self, dish: dict):
        self.__save(Event.COOSE_DISH, dish)
        self.__dishes.append(dish)

    @property
    def dishes(self):
        return self.__dishes

    @property
    def user(self) -> User:
        return self.__user

    @property
    def price(self) -> float:
        return sum((float(p['price']) for p in self.__dishes))

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str):
        self.__address = value
