class BaseURL:
    BASE_URL = "https://qa-stellarburgers.education-services.ru/api"


class ApiURL:
    ORDER_URL = f"{BaseURL.BASE_URL}/orders"
    REGISTER_URL = f"{BaseURL.BASE_URL}/auth/register"
    LOGIN_URL = f"{BaseURL.BASE_URL}/auth/login"
    USER_URL = f"{BaseURL.BASE_URL}/auth/user"
    INGRIDIENTS_URL = f"{BaseURL.BASE_URL}/ingredients"
