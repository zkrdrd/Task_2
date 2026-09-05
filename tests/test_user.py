import allure  # pylint: disable=import-error
import pytest  # pylint: disable=import-error

from helpers.base import ApiURL
from helpers.data import MessageResponse
from helpers.helper import generate_unique_email, get, patch, post


@allure.feature("Управление пользователями")
class TestCreateUser:
    @allure.story("Создание пользователя")
    @allure.title("Успешное создание уникального пользователя")
    @allure.description(
        "Проверка, что можно создать нового пользователя с корректными данными"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_success(self, new_user_data):
        """Успешное создание уникального пользователя."""
        data = post(ApiURL.REGISTER_URL, json=new_user_data)
        assert data["success"] is True
        assert "accessToken" in data
        assert "refreshToken" in data
        assert data["user"]["email"] == new_user_data["email"]
        assert data["user"]["name"] == new_user_data["name"]

    @allure.story("Создание пользователя")
    @allure.title("Создание уже зарегистрированного пользователя")
    @allure.description(
        "Проверка, что повторная регистрация с теми же данными возвращает ошибку"
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_duplicate(self, registered_and_delete_user):
        """Создание уже зарегистрированного пользователя."""
        data = post(
            ApiURL.REGISTER_URL,
            json={
                "email": registered_and_delete_user["email"],
                "password": registered_and_delete_user["password"],
                "name": registered_and_delete_user["name"],
            },
        )
        assert data["success"] is False
        assert MessageResponse.USER_EXIST in data["message"]

    @allure.story("Создание пользователя")
    @allure.title("Создание пользователя без обязательного поля: {missing_field}")
    @allure.description("Проверка, что отсутствие обязательного поля приводит к ошибке")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field(self, missing_field, new_user_data):
        """Создание пользователя без одного обязательного поля."""
        payload = new_user_data.copy()
        del payload[missing_field]
        data = post(ApiURL.REGISTER_URL, json=payload)
        assert data["success"] is False
        assert MessageResponse.REQUIRED_FIELD in data["message"]


@allure.feature("Аутентификация")
class TestLogin:
    @allure.story("Вход в систему")
    @allure.title("Успешный вход с корректными данными")
    @allure.description("Проверка, что существующий пользователь может войти")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_existing_user(self, registered_and_delete_user):
        """Логин под существующим пользователем."""
        data = post(
            ApiURL.LOGIN_URL,
            json={
                "email": registered_and_delete_user["email"],
                "password": registered_and_delete_user["password"],
            },
        )
        assert data["success"] is True
        assert "accessToken" in data
        assert data["user"]["email"] == registered_and_delete_user["email"]

    @allure.story("Вход в систему")
    @allure.title("Вход с неверным email")
    @allure.description("Проверка, что вход с неправильным email отклоняется")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_wrong_email(self, registered_and_delete_user):
        """Логин с неверным email."""
        payload = {
            "email": "wrong_" + registered_and_delete_user["email"],
            "password": registered_and_delete_user["password"],
        }
        data = post(ApiURL.LOGIN_URL, json=payload)
        assert data["success"] is False
        assert MessageResponse.EMAIL_PASSWORD_INCORRECT in data["message"]

    @allure.story("Вход в систему")
    @allure.title("Вход с неверным паролем")
    @allure.description("Проверка, что вход с неправильным паролем отклоняется")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_wrong_password(self, registered_and_delete_user):
        """Логин с неверным паролем."""
        payload = {
            "email": registered_and_delete_user["email"],
            "password": "wrong_password",
        }
        data = post(ApiURL.LOGIN_URL, json=payload)
        assert data["success"] is False
        assert MessageResponse.EMAIL_PASSWORD_INCORRECT in data["message"]


@allure.feature("Управление профилем")
class TestUpdateUser:
    @allure.story("Изменение данных пользователя")
    @allure.title("Изменение email с авторизацией")
    @allure.description(
        "Проверка, что авторизованный пользователь может изменить email"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_user_email_with_auth(
        self, registered_and_delete_user, auth_headers
    ):
        """Изменение email с авторизацией."""
        new_email = generate_unique_email()
        data = patch(
            ApiURL.USER_URL,
            json={"email": new_email},
            headers=auth_headers,
        )
        assert data["success"] is True
        assert data["user"]["email"] == new_email

    @allure.story("Изменение данных пользователя")
    @allure.title("Изменение имени с авторизацией")
    @allure.description("Проверка, что авторизованный пользователь может изменить имя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user_name_with_auth(self, registered_and_delete_user, auth_headers):
        """Изменение имени с авторизацией."""
        new_name = "New Name"
        data = patch(
            ApiURL.USER_URL,
            json={"name": new_name},
            headers=auth_headers,
        )
        assert data["success"] is True
        assert data["user"]["name"] == new_name

    @allure.story("Изменение данных пользователя")
    @allure.title("Изменение пароля с авторизацией")
    @allure.description(
        "Проверка, что авторизованный пользователь может изменить пароль и войти с новым паролем"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_user_password_with_auth(
        self, registered_and_delete_user, auth_headers
    ):
        """Изменение пароля с авторизацией."""
        new_password = "new_password123"
        data = patch(
            ApiURL.USER_URL,
            json={"password": new_password},
            headers=auth_headers,
        )
        assert data["success"] is True
        login_response = post(
            ApiURL.LOGIN_URL,
            json={
                "email": registered_and_delete_user["email"],
                "password": new_password,
            },
        )
        assert login_response["success"] is True

    @allure.story("Изменение данных пользователя")
    @allure.title("Изменение данных без авторизации")
    @allure.description(
        "Проверка, что неавторизованный запрос на изменение данных отклоняется"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_user_without_auth(self):
        """Изменение данных без авторизации."""
        data = patch(ApiURL.USER_URL, json={"name": "No Auth"})
        assert data["success"] is False
        assert MessageResponse.SHOULD_BE_AUTORIZED in data["message"]
