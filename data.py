class RequestAndResponseKeys:

    EMAIL = 'email'
    PASSWORD = 'password'
    NAME = 'name'
    ACCESS_TOKEN = 'accessToken'
    ACCESS_TOKEN_TYPE = 'Bearer '
    SUCCESS = 'success'
    AUTH_FIELD_NAME = 'Authorization'
    USER = 'user'
    REF_TOKEN = 'refreshToken'
    MESSAGE = 'message'
    DATA = 'data'
    TYPE = 'type'
    BUN = 'bun'
    FILLING = 'main'
    SAUCE = 'sauce'
    ID = '_id'
    INGREDIENTS = 'ingredients'
    ORDER = 'order'
    NUMBER = 'number'


class StatusCodes:

    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    ERROR_500 = 500


class Messages:

    USER_EXISTS = 'User already exists'
    EMPTY_FIELD = 'Email, password and name are required fields'
    INCORRECT_EMAIL_OR_PASS = 'email or password are incorrect'
    EMPTY_BURGER = 'Ingredient ids must be provided'
