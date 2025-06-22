import requests

from data import RequestAndResponseKeys as Key
from urls import Url


class CreateUser:

    # Отправляем запрос на создание уникального пользователя
    @staticmethod
    def register_new_user(user_data):
        return requests.post(f'{Url.REGISTER_USER}', data=user_data)

class DeleteUser:

    # Отправляем запрос на удаление существующего пользователя
    @staticmethod
    def delete_user(access_token):
        return requests.delete(f'{Url.DELETE_USER}', headers={Key.AUTH_FIELD_NAME: access_token})

class LoginUser:

    # Отправляем запрос на авторизацию существующего пользователя
    @staticmethod
    def auth_user(email, password):
        data = {Key.EMAIL: email, Key.PASSWORD: password}
        return requests.post(f'{Url.LOGIN_USER}', data=data)