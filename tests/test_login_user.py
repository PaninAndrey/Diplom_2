import pytest
import allure

from data import RequestAndResponseKeys as Key, StatusCodes as SC, Messages as M
from helper_methods import HelperMethods as Help
from user_methods import LoginUser as LU
from generators import generate_fake_data


class TestLoginUser:

    @allure.title('Проверка входа под существующим пользователем')
    def test_login_user_successfully(self, generate_user):
        with allure.step('Получаем набор данных зарегистрированного уникального пользователя'):
            user_data = generate_user[0]
        with allure.step('Получаем "email" и "name" зарегистрированного пользователя для авторизации'):
            email = user_data[Key.EMAIL]
            password = user_data[Key.PASSWORD]
        with allure.step('Отправляем запрос на авторизацию пользователя'):
            response = LU.auth_user(email, password)
        with allure.step('Проверяем код статуса полученного ответа при авторизации пользователя - 200'):
            Help.check_status_code(response, SC.OK)
        with allure.step('Проверяем, что в теле ответа содержится ключ "success" со значением "True" и присваиваем его переменной'):
            response_value = Help.is_key_in_response_body(response.json(), Key.SUCCESS)
        with allure.step('Проверяем фактическое значение ключа "success" в теле ответа с ожидаемым - "True"'):
            assert response_value, f'Неверное значение ключа "{Key.SUCCESS}" в теле ответа'


    @allure.title('Проверка входа с неверным логином или паролем')
    @pytest.mark.parametrize('field_name', [
        Key.EMAIL,
        Key.PASSWORD,
    ])
    def test_no_login_without_login_and_password(self, generate_user, field_name):
        with allure.step('Получаем набор данных созданного уникального пользователя'):
            user_data = generate_user[0]
        with allure.step('Удаляем из набора данных созданного уникального пользователя поле "name"'):
            user_data.pop(Key.NAME)
        with allure.step('Присваиваем проверяемым полям "email" и "password" неверные значения'):
            user_data[field_name] = generate_fake_data()
        with allure.step('Отправляем запрос на авторизацию пользователя'):
            response = LU.auth_user(user_data[Key.EMAIL], user_data[Key.PASSWORD])
        with allure.step('Проверяем код статуса полученного ответа при неудавшейся авторизации пользователя - 401'):
            Help.check_status_code(response, SC.UNAUTHORIZED)
        with allure.step('Проверяем, что в теле ответа содержится ключ "success" со значением "False" и присваиваем его переменной'):
            response_value = Help.is_key_in_response_body(response.json(), Key.SUCCESS)
        with allure.step('Проверяем фактическое значение ключа "success" в теле ответа с ожидаемым - "False"'):
            assert not response_value, f'Неверное значение ключа "{Key.SUCCESS}" в теле ответа'
        with allure.step('Проверяем, что в теле ответа содержится ключ "message", получаем его значение и присваиваем его переменной'):
            response_message = Help.is_key_in_response_body(response.json(), Key.MESSAGE)
        with allure.step('Проверяем фактическое значение ключа "message" в теле ответа с ожидаемым'):
            assert response_message == M.INCORRECT_EMAIL_OR_PASS, f'Неверный текст поля {Key.MESSAGE}'
