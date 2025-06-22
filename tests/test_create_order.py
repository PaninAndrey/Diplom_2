import allure

from data import RequestAndResponseKeys as Key, StatusCodes as SC, Messages as M
from order_methods import CreateOrder as CO
from helper_methods import HelperMethods as Help
from generators import generate_invalid_ingredient_hash


class TestCreateOrder:

    @allure.title('Проверяем создание заказа с ингредиентами авторизованным пользователем')
    def test_create_new_order_by_auth_user_and_ingredients_true(self, generate_user):
        with allure.step('Получаем "accessToken" зарегистрированного уникального пользователя'):
            access_token = generate_user[2]
        with allure.step('Создаем бургер для оформления заказа'):
            burger = Help.generate_burger()
        with allure.step('Отправляем запрос на создание заказа'):
            response = CO.make_an_order(burger, headers={Key.AUTH_FIELD_NAME: access_token})
        with allure.step('Проверяем статус полученного ответа - 200'):
            Help.check_status_code(response, SC.OK)
        with allure.step('Проверяем, что в теле ответа содержится ключ "success" и присваиваем его значение переменной'):
            response_value = Help.is_key_in_response_body(response.json(), Key.SUCCESS)
        with allure.step('Проверяем фактическое значение ключа "success" в теле ответа с ожидаемым - "True"'):
            assert response_value, f'Неверное значение ключа "{Key.SUCCESS}" в теле ответа'
        with allure.step('Проверяем, что в теле ответа содержится ключ "name" и присваиваем его значение переменной'):
            order_name = Help.is_key_in_response_body(response.json(), Key.NAME)
        with allure.step('Проверяем, что фактическое значение ключа "name" - строка"'):
            assert type(order_name) is str, f'Неверный формат значения ключа "{Key.NAME}" в теле ответа'
        with allure.step('Проверяем, что в теле ответа содержится ключ "order" и присваиваем его значение переменной'):
            order_list = Help.is_key_in_response_body(response.json(), Key.ORDER)
        with allure.step('Проверяем, что фактическое значение ключа "name" - cловарь'):
            assert type(order_list) is dict, f'Неверный формат значения ключа "{Key.ORDER}" в теле ответа'
        with allure.step('Проверяем, что в теле ответа в словаре по ключу "order" содержится ключ "number" и присваиваем его значение переменной'):
            order_number = Help.is_key_in_response_body(order_list, Key.NUMBER)
        with allure.step('Проверяем, что фактическое значение ключа "number" - число'):
            assert str(order_number).isdigit(), f'Неверный формат значения ключа "{Key.NUMBER}" в теле ответа'


    @allure.title('Проверяем создание заказа без ингредиентов авторизованным пользователем')
    def test_create_new_order_by_auth_user_with_no_ingredients(self, generate_user):
        with allure.step('Получаем "accessToken" зарегистрированного уникального пользователя'):
            access_token = generate_user[2]
        with allure.step('Создаем пустой бургер для оформления заказа'):
            burger = []
        with allure.step('Отправляем запрос на создание заказа'):
            response = CO.make_an_order(burger, headers={Key.AUTH_FIELD_NAME: access_token})
        with allure.step('Проверяем статус полученного ответа - 400'):
            Help.check_status_code(response, SC.BAD_REQUEST)
        with allure.step('Проверяем, что в теле ответа содержится ключ "success" и присваиваем его значение переменной'):
            response_value = Help.is_key_in_response_body(response.json(), Key.SUCCESS)
        with allure.step('Проверяем фактическое значение ключа "success" в теле ответа с ожидаемым - "False"'):
            assert not response_value, f'Неверное значение ключа "{Key.SUCCESS}" в теле ответа'
        with allure.step('Проверяем, что в теле ответа содержится ключ "messasge" и присваиваем его значение переменной'):
            response_message = Help.is_key_in_response_body(response.json(), Key.MESSAGE)
        with allure.step('Проверяем, что текст сообщения об ошибке соответствует ожидаемому'):
            assert response_message == M.EMPTY_BURGER, f'Неверный текст поля {Key.MESSAGE}'


    @allure.title('Проверяем создание заказа с ингредиентами НЕавторизованным пользователем')
    def test_create_new_order_by_unauth_user_and_ingredients_true(self):
        with allure.step('Создаем бургер для оформления заказа'):
            burger = Help.generate_burger()
        with allure.step('Отправляем запрос на создание заказа'):
            response = CO.make_an_order(burger)
        with allure.step('Проверяем статус полученного ответа - 200'):
            Help.check_status_code(response, SC.OK)
        with allure.step('Проверяем, что в теле ответа содержится ключ "success" и присваиваем его значение переменной'):
            response_value = Help.is_key_in_response_body(response.json(), Key.SUCCESS)
        with allure.step('Проверяем фактическое значение ключа "success" в теле ответа с ожидаемым - "True"'):
            assert response_value, f'Неверное значение ключа "{Key.SUCCESS}" в теле ответа'
        with allure.step('Проверяем, что в теле ответа содержится ключ "name" и присваиваем его значение переменной'):
            order_name = Help.is_key_in_response_body(response.json(), Key.NAME)
        with allure.step('Проверяем, что фактическое значение ключа "name" - строка"'):
            assert type(order_name) is str, f'Неверный формат значения ключа "{Key.NAME}" в теле ответа'
        with allure.step('Проверяем, что в теле ответа содержится ключ "order" и присваиваем его значение переменной'):
            order_list = Help.is_key_in_response_body(response.json(), Key.ORDER)
        with allure.step('Проверяем, что фактическое значение ключа "name" - cловарь'):
            assert type(order_list) is dict, f'Неверный формат значения ключа "{Key.ORDER}" в теле ответа'
        with allure.step('Проверяем, что в теле ответа в словаре по ключу "order" содержится ключ "number" и присваиваем его значение переменной'):
            order_number = Help.is_key_in_response_body(order_list, Key.NUMBER)
        with allure.step('Проверяем, что фактическое значение ключа "number" - число'):
            assert str(order_number).isdigit(), f'Неверный формат значения ключа "{Key.NUMBER}" в теле ответа'


    @allure.title('Проверяем создание заказа без ингредиентов НЕавторизованным пользователем')
    def test_create_new_order_by_unauth_user_with_no_ingredients(self):
        with allure.step('Создаем пустой бургер для оформления заказа'):
            burger = []
        with allure.step('Отправляем запрос на создание заказа'):
            response = CO.make_an_order(burger)
        with allure.step('Проверяем статус полученного ответа - 400'):
            Help.check_status_code(response, SC.BAD_REQUEST)
        with allure.step('Проверяем, что в теле ответа содержится ключ "success" и присваиваем его значение переменной'):
            response_value = Help.is_key_in_response_body(response.json(), Key.SUCCESS)
        with allure.step('Проверяем фактическое значение ключа "success" в теле ответа с ожидаемым - "False"'):
            assert not response_value, f'Неверное значение ключа "{Key.SUCCESS}" в теле ответа'
        with allure.step('Проверяем, что в теле ответа содержится ключ "messasge" и присваиваем его значение переменной'):
            response_message = Help.is_key_in_response_body(response.json(), Key.MESSAGE)
        with allure.step('Проверяем, что текст сообщения об ошибке соответствует ожидаемому'):
            assert response_message == M.EMPTY_BURGER, f'Неверный текст поля {Key.MESSAGE}'


    @allure.title('Проверяем создание заказа с неверным хешем ингредиентов')
    def test_create_new_order_with_invalid_ingredients_hash(self):
        with allure.step('Создаем бургер с неверным хешем ингредиентов'):
            burger = [generate_invalid_ingredient_hash()]
        with allure.step('Отправляем запрос на создание заказа'):
            response = CO.make_an_order(burger)
        with allure.step('Проверяем статус полученного ответа - 500'):
            Help.check_status_code(response, SC.ERROR_500)
