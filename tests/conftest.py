import pytest

from generators import UserData as UD
from user_methods import CreateUser as CU, DeleteUser as DU
from helper_methods import HelperMethods as Help
from data import StatusCodes as SC


### Создаем пользователя и сохраняем его данные для удаления после завершения тестов ###
@pytest.fixture
def generate_user():
    # Генерируем email, пароль и имя нового пользователя
    user_data = UD.generate_new_user_data()
    # Отправляем запрос на создание уникального пользователя
    response = CU.register_new_user(user_data)
    # Проверяем код статуса полученного ответа при созданиии уникального пользователя - 200
    Help.check_status_code(response, SC.OK)
    # Получаем тело ответа в формате словаря
    response_dict = response.json()
    # Получаем авторизационный токен
    access_token = Help.get_access_token(response_dict)
    # Возвращаем данные пользователя, тело успешного ответа на запрос на создание пользователя и авторизационный токен
    yield [user_data, response_dict, access_token]
    # Удаляем созданного пользователя после завершения теста
    DU.delete_user(access_token)
