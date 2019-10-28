import requests
from datetime import datetime
from telebot.types import User
from context import Context
from functools import lru_cache
from utils import logger

test_date = datetime(year=2019, month=10, day=21)


class Service(object):
    def __init__(self, base_url='http://127.0.0.1:8000/api'):
        self.__base_url = base_url
        self.__categories = self.__download_categories()

    @lru_cache(maxsize=None)
    @logger
    def __download_menu(self, day: datetime = datetime.now()) -> list:
        day = test_date  # FIXME
        sday = day.strftime("%Y-%m-%d")
        response = requests.get(
            f'{self.__base_url}/days/?format=json&day={sday}')
        menu = []
        if response.ok:
            response_json = response.json()
            for dish_url in response_json[0]['dishes']:
                dish = requests.get(dish_url).json()
                dish['category'] = requests.get(dish['category']).json()
                menu.append(dish)
        return menu

    @lru_cache(maxsize=None)
    @logger
    def __download_categories(self) -> list:
        response = requests.get(f'{self.__base_url}/categories/?format=json')
        # print(json.text)
        if response.ok:
            return response.json()
        return []

    @property
    def menu(self) -> list:
        return self.__download_menu()

    @property
    def categories(self) -> list:
        '''
        Return list categories
        '''
        return self.__categories

    def dish(self, id: int):
        '''
        Return dish by id
        '''
        return next(d for d in self.menu if d['id'] == id)

    @logger
    def make_order(self, ctx: Context):
        date = datetime.now()
        json = {
            "date": date.isoformat(),
            "dishes": [f"{self.__base_url}/dishes/{d['id']}/" for d in ctx.dishes],
            "client_id": ctx.user.id,
            "address": ctx.address
        }
        response = requests.post(f'{self.__base_url}/orders/', json=json)
        return response.json()
