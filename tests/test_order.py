import allure  # pylint: disable=import-error

from helpers.base import ApiURL
from helpers.data import MessageResponse
from helpers.helper import get, post


@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.story("Создание заказа")
    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    @allure.description(
        "Проверка, что авторизованный пользователь может создать заказ с корректными ингредиентами"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_auth(
        self, registered_and_delete_user, auth_headers, ingredients
    ):
        """Создание заказа с авторизацией и валидными ингредиентами."""
        data = post(
            ApiURL.ORDER_URL, json={"ingredients": ingredients}, headers=auth_headers
        )
        assert data["success"] is True
        assert "order" in data
        assert data["order"]["owner"]["email"] == registered_and_delete_user["email"]

    @allure.story("Создание заказа")
    @allure.title("Создание заказа без авторизации")
    @allure.description("Проверка, что можно создать заказ без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_auth(self, ingredients):
        """Создание заказа без авторизации."""
        data = post(ApiURL.ORDER_URL, json={"ingredients": ingredients})
        assert data["success"] is True
        assert "order" in data
        assert data["order"].get("owner") is None

    @allure.story("Создание заказа")
    @allure.title("Создание заказа с пустым списком ингредиентов")
    @allure.description("Проверка, что заказ без ингредиентов отклоняется")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_no_ingredients(self, auth_headers):
        """Создание заказа с пустым списком ингредиентов."""
        data = post(ApiURL.ORDER_URL, json={"ingredients": []}, headers=auth_headers)
        assert data["success"] is False
        assert MessageResponse.INGREDIENT_MUST_PROVIDED in data["message"]

    @allure.story("Создание заказа")
    @allure.title("Создание заказа с неверным хешем ингредиента")
    @allure.description("Проверка, что невалидный хеш ингредиента приводит к ошибке")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_invalid_ingredient_hash(self, auth_headers):
        """Создание заказа с неверным хешем ингредиента."""
        data = post(
            ApiURL.ORDER_URL,
            json={"ingredients": ["invalid_hash"]},
            headers=auth_headers,
        )
        assert data["success"] is False


@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:
    @allure.story("Получение заказов")
    @allure.title("Получение заказов авторизованного пользователя")
    @allure.description(
        "Проверка, что авторизованный пользователь может получить список своих заказов"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_orders_with_auth(
        self, registered_and_delete_user, auth_headers, ingredients
    ):
        """Получение заказов авторизованного пользователя."""
        post(
            ApiURL.ORDER_URL,
            json={"ingredients": ingredients},
            headers=auth_headers,
        )
        data = get(ApiURL.ORDER_URL, headers=auth_headers)
        assert data["success"] is True
        assert "orders" in data
        assert len(data["orders"]) >= 1

    @allure.story("Получение заказов")
    @allure.title("Получение заказов без авторизации")
    @allure.description(
        "Проверка, что неавторизованный запрос на получение заказов отклоняется"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_orders_without_auth(self):
        """Получение заказов без авторизации."""
        data = get(ApiURL.ORDER_URL)
        assert data["success"] is False
        assert MessageResponse.SHOULD_BE_AUTORIZED in data["message"]
