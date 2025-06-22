import pytest
import allure

from data import RequestAndResponseKeys as Key, StatusCodes as SC, Messages as M
from helper_methods import HelperMethods as Help
from user_methods import CreateUser as CU, DeleteUser as DU
from generators import UserData as UD


class TestCreateUser:

    @allure.title('Проверяем, что при регистрации уникального пользователя в теле ответа есть ключ "success" со значением "True"')
    def test_create_new_user_success_true(self):
        with allure.step('Генерируем данные пользователя'):
            user_data = UD.generate_new_user_data()
        with allure.step('Отправляем запрос на создание уникального пользователя'):
            response = CU.register_new_user(user_data)
        with allure.step('Проверяем код статуса полученного ответа при созданиии уникального пользователя - 200'):
            Help.check_status_code(response, SC.OK)
        with allure.step('Проверяем, что в теле ответа содержится ключ "success" со значением "True" и присваиваем его переменной'):
            response_value = Help.is_key_in_response_body(response.json(), Key.SUCCESS)
        with allure.step('Получаем авторизационный токен'):
            access_token = Help.get_access_token(response.json())
        with allure.step('Удаляем созданного пользователя'):
            DU.delete_user(access_token)
        with allure.step('Проверяем фактическое значение ключа "success" в теле ответа с ожидаемым - "True"'):
            assert response_value, f'Неверное значение ключа {Key.SUCCESS} в теле ответа'


    @allure.title('Проверяем, что при регистрации уникального пользователя в теле ответа вернулись "email" и "name", отправленные в запросе на регистрацию')
    def test_create_new_user_get_email_and_name_successfully(self):
        with allure.step('Генерируем данные пользователя'):
            user_data = UD.generate_new_user_data()
        with allure.step('Отправляем запрос на создание уникального пользователя'):
            response = CU.register_new_user(user_data)
        with allure.step('Проверяем код статуса полученного ответа при созданиии уникального пользователя - 200'):
            Help.check_status_code(response, SC.OK)
        with allure.step('Получаем тело ответа в формате словаря'):
            response_body = response.json()
        with allure.step('Проверяем, что в теле ответа содержится ключ "user"'):
            assert Key.USER in response_body, f'В теле ответа отсутствует ключ {Key.USER}'
        with allure.step('Проверяем, что в теле ответа ключ "user" представлен в виде словаря'):
            assert type(Help.is_key_in_response_body(response_body, Key.USER)) is dict, f'Данные в ответе на запрос в поле {Key.USER} представлены не в виде словаря'
        with allure.step('Назначаем переменную, полученному по ключу "user" словарю'):
            user_dict = Help.is_key_in_response_body(response_body, Key.USER)
        with allure.step('Получаем значение "email" из набора данных, отправленных в запросе на регистрацию уникального пользователя'):
            email = user_data[Key.EMAIL]
        with allure.step('Получаем значение "email" из словаря "user" в теле ответа'):
            email_response = user_dict[Key.EMAIL]
        with allure.step('Проверяем, что "email", указанный в запросе, и "email", полученный в теле ответа на запрос, совпадают'):
            assert email == email_response, f'"{email}", указанный в запросе, и "{email}", полученный в теле ответа на запрос, НЕ совпадают'
        with allure.step('Получаем значение "name" из набора данных, отправленных в запросе на регистрацию уникального пользователя'):
            name = user_data[Key.NAME]
        with allure.step('Получаем значение "name" из словаря "user" в теле ответа'):
            name_response = user_dict[Key.NAME]
        with allure.step('Проверяем, что "name", указанное в запросе, и "name", полученное в теле ответа на запрос, совпадают'):
            assert name == name_response, f'"{name}", указанное в запросе, и "{name_response}", полученное в теле ответа на запрос, НЕ совпадают'


    @allure.title('Проверяем, что при регистрации уникального пользователя в теле ответа вернулcя "refreshToken"')
    def test_create_new_user_get_refresh_token_successfully(self, generate_user):
        with allure.step('Получаем содержимое ответа на запрос на создание уникального пользователя в виде словаря'):
            response_body = generate_user[1]
        with allure.step('Проверяем, что в теле ответа содержится ключ "refreshToken"'):
            assert Key.REF_TOKEN in response_body, f'В теле ответа отсутствует ключ {Key.REF_TOKEN}'
        with allure.step('Проверяем, что в теле ответа ключ "refreshToken" представлен в виде непустой строки'):
            assert (type(Help.is_key_in_response_body(response_body, Key.REF_TOKEN)) is str and
                    len(Help.is_key_in_response_body(response_body, Key.REF_TOKEN)) > 0), f'Данные в ответе на запрос в поле {Key.REF_TOKEN} представлены в неверном формате'


    @allure.title('Проверяем создание пользователя, который уже зарегистрирован')
    def test_create_existing_user(self, generate_user):
        with allure.step('Получаем набор данных созданного уникального пользователя'):
            user_data = generate_user[0]
        with allure.step('Отправляем повторный запрос на создание уже существующего пользователя'):
            response = CU.register_new_user(user_data)
        with allure.step('Проверяем код статуса полученного ответа при созданиии существующего пользователя - 403'):
            Help.check_status_code(response, SC.FORBIDDEN)
        with allure.step('Проверяем, что в теле ответа содержится ключ "success" со значением "False" и присваиваем его переменной'):
            response_value = Help.is_key_in_response_body(response.json(), Key.SUCCESS)
        with allure.step('Проверяем фактическое значение ключа "success" в теле ответа с ожидаемым - "False"'):
            assert not response_value, f'Неверное значение ключа "{Key.SUCCESS}" в теле ответа'
        with allure.step('Проверяем, что в теле ответа содержится ключ "message", получаем его значение и присваиваем его переменной'):
            response_message = Help.is_key_in_response_body(response.json(), Key.MESSAGE)
        with allure.step('Проверяем фактическое значение ключа "message" в теле ответа с ожидаемым'):
            assert response_message == M.USER_EXISTS, f'Неверный текст поля {Key.MESSAGE}'


    @allure.title('Проверяем невозможность создания пользователя с одним из незаполненныз обязательных полей')
    @pytest.mark.parametrize('field_name', [
        Key.EMAIL,
        Key.PASSWORD,
        Key.NAME
    ])
    def test_impossible_to_create_new_user_with_any_empty_field(self, field_name):
        with allure.step('Генерируем данные для создания уникального пользователя'):
            user_data = UD.generate_new_user_data()
        with allure.step('Удаляем из сгенерированныж данных пользователя необходимое поле'):
            user_data.pop(field_name)
        with allure.step('Отправляем в систему запрос на создание уникального пользователя'):
            response = CU.register_new_user(user_data)
        with allure.step('Проверяем код статуса полученного ответа при созданиии пользователя без заполненного поля - 403'):
            Help.check_status_code(response, SC.FORBIDDEN)
        with allure.step('Проверяем, что в теле ответа содержится ключ "success" со значением "False" и присваиваем его переменной'):
            response_value = Help.is_key_in_response_body(response.json(), Key.SUCCESS)
        with allure.step('Проверяем фактическое значение ключа "success" в теле ответа с ожидаемым - "False"'):
            assert not response_value, f'Неверное значение ключа "{Key.SUCCESS}" в теле ответа'
        with allure.step('Проверяем, что в теле ответа содержится ключ "message", получаем его значение и присваиваем его переменной'):
            response_message = Help.is_key_in_response_body(response.json(), Key.MESSAGE)
        with allure.step('Проверяем фактическое значение ключа "message" в теле ответа с ожидаемым'):
            assert response_message == M.EMPTY_FIELD, f'Неверный текст поля {Key.MESSAGE}'
