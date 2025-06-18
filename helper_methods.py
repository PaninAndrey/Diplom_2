from data import RequestAndResponseKeys as Key
from order_methods import IngredientsData as ID


class HelperMethods:

    # Проверяем код ответа
    @staticmethod
    def check_status_code(response, expected_code):
        # Получаем код ответа
        received_code = response.status_code
        # Проверяем, что получен код ответа expected_code
        assert received_code == expected_code, f'Неверный код cтатуса в ответе: ожидаемый - "{expected_code}", фактический- "{received_code}"'


    # Проверяем наличие ключа в теле ответа
    @staticmethod
    def is_key_in_response_body(response, key):
        # Проверям, что в теле ответа присутствует ключ key
        assert key in response, f'В теле ответа отсутствует ключ "{key}"'
        # Возвращаем значение ключа key
        return response[key]


    # Проверяем наличие в теле ответа ключа "accessToken" и получаем его значение
    @staticmethod
    def get_access_token(response):
        # Проверяем наличие в теле ответа ключа "accessToken" и получаем его значение
        access_token = HelperMethods.is_key_in_response_body(response, Key.ACCESS_TOKEN)
        # Проверяем, что тип авторизационного токена - строка, начинается со слова "Bearer "
        # и его длина больше, чем длина слова "Bearer " c учетом пробела
        assert  (type(access_token) is str and
                Key.ACCESS_TOKEN_TYPE in access_token and
                len(access_token) > len(Key.ACCESS_TOKEN_TYPE)), f'Получено неверное значение ключа авторизационного токена {Key.ACCESS_TOKEN}'
        return access_token


    # Получаем данные об ингредиентах
    @staticmethod
    def get_ingredients_list():
        # Отправляем запрос на получение данных об ингредиентах
        response = ID.get_ingredients_list()
        # Преобразуем полученный ответ в словарь
        response_list = response.json()
        # Проверяем, что в полученном словара присутствует ключ "data" и возвращаем его значение в виде списка продуктов
        ingredients_list = HelperMethods.is_key_in_response_body(response_list, Key.DATA)
        return ingredients_list


    # Получаем список булок из общего списка ингредиентов
    @staticmethod
    def get_buns_list():
        # Инициализируем пустой список булок
        buns_list = []
        # Объявляем переменную для списка из всех продуктов
        ingredients_list = HelperMethods.get_ingredients_list()
        # Выбираем в цикле из всего списка продуктов булочки и добавляем их в список булок
        for item in ingredients_list:
            if item[Key.TYPE] == Key.BUN:
                buns_list.append(item)
        return buns_list


    # Получаем список начинок из общего списка ингредиентов
    @staticmethod
    def get_fillings_list():
        # Инициализируем пустой список начинок
        fillings_list = []
        # Объявляем переменную для списка из всех продуктов
        ingredients_list = HelperMethods.get_ingredients_list()
        # Выбираем в цикле из всего списка продуктов начинки и добавляем их в список начинок
        for item in ingredients_list:
            if item[Key.TYPE] == Key.FILLING:
                fillings_list.append(item)
        return fillings_list


    # Получаем список соусов из общего списка ингредиентов
    @staticmethod
    def get_sauces_list():
        # Инициализируем пустой список соусов
        sauces_list = []
        # Объявляем переменную для списка из всех продуктов
        ingredients_list = HelperMethods.get_ingredients_list()
        # Выбираем в цикле из всего списка продуктов coусы и добавляем их в список соусов
        for item in ingredients_list:
            if item[Key.TYPE] == Key.SAUCE:
                sauces_list.append(item)
        return sauces_list


    ### Создаем бургер из двух булочек, двух начинок и двух соусов для проверки создания заказа ###
    @staticmethod
    def generate_burger():
        # Инициализируем пустой список для создания бургера
        burger = []
        # Получаем хеш булочки
        bun = HelperMethods.get_buns_list()[1][Key.ID]
        # Добавляем в бургер две булочки
        burger.append(bun)
        burger.append(bun)
        # Получаем хеш начинок
        filling_1 = HelperMethods.get_fillings_list()[0][Key.ID]
        filling_2 = HelperMethods.get_fillings_list()[1][Key.ID]
        # Добавляем в бургер две начинки
        burger.append(filling_1)
        burger.append(filling_2)
        # Получаем хеш соусов
        sauce_1 = HelperMethods.get_sauces_list()[0][Key.ID]
        sauce_2 = HelperMethods.get_sauces_list()[1][Key.ID]
        # Добавляем в бургер два соуса
        burger.append(sauce_1)
        burger.append(sauce_2)
        # Возвращаем собранный бургер
        return burger
