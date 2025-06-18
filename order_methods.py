import requests
import allure

from data import Url, RequestAndResponseKeys as Key


class IngredientsData:

    @staticmethod
    @allure.step('Отправляем запрос на получение данных об ингредиентах')
    def get_ingredients_list():
        return requests.get(f'{Url.BASE_URL}{Url.GET_INGREDIENTS}')


class CreateOrder:
    @staticmethod
    @allure.step('Отправляем запрос на создание заказа')
    def make_an_order(burger, headers=None):
        return requests.post(f'{Url.BASE_URL}{Url.MAKE_ORDER}', headers=headers, data={Key.INGREDIENTS: burger})
