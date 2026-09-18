import pytest  # pylint: disable=import-error

from helpers.base import ApiURL
from helpers.helper import (
    delete,
    generate_random_string,
    generate_unique_email,
    get,
    post,
)


@pytest.fixture
def new_user_data():
    """Генерирует данные для нового пользователя."""
    return {
        "email": generate_unique_email(),
        "password": generate_random_string(),
        "name": generate_random_string(),
    }


@pytest.fixture
def registered_and_delete_user(new_user_data):
    """Создаёт пользователя и возвращает его данные вместе с токенами."""
    data = post(ApiURL.REGISTER_URL, json=new_user_data)
    new_user_data["accessToken"] = data["accessToken"]
    new_user_data["refreshToken"] = data["refreshToken"]
    new_user_data["user"] = data["user"]
    yield new_user_data
    post(
        ApiURL.LOGIN_URL,
        json={
            "email": new_user_data["email"],
            "password": new_user_data["password"],
        },
    )
    delete(ApiURL.USER_URL)


@pytest.fixture
def auth_headers(registered_and_delete_user):
    """Заголовки с авторизацией для зарегистрированного пользователя."""
    return {"Authorization": registered_and_delete_user["accessToken"]}


@pytest.fixture
def ingredients():
    """Получает список валидных ID ингредиентов."""
    data = get(ApiURL.INGRIDIENTS_URL)
    return [ing["_id"] for ing in data["data"][:2]]
