import allure
import pytest
import requests

from test.conftest import ApiClient
from urls import base_url_scooter


api_client = ApiClient(base_url_scooter)


class TestLoginCourier:
    @allure.title('Проверка на успешный логин созданного курьера с возвратом id')
    def test_login_courier(self, create_courier, delete_courier):
        response, courier_data = create_courier
        login = courier_data["login"]
        password = courier_data["password"]

        url = api_client.go_to_url("/api/v1/courier/login")
        payload = {
            "login": login,
            "password": password,
        }

        login_response = requests.post(url, json=payload)
        response_json = login_response.json()
        courier_id = response_json.get("id")
        assert courier_id is not None, "Ошибка: 'id' не найдено в ответе"
        expected_response = {"id": courier_id}
        assert response_json == expected_response, f"Ошибка: ответ {response_json} не соответствует {expected_response}"

        delete_courier(courier_id)

    @pytest.mark.parametrize(
        "login, password, expected_message",
        [
            (None, "somepassword", "Недостаточно данных для входа"),
            ("", "somepassword", "Недостаточно данных для входа"),
            ("validlogin", "", "Недостаточно данных для входа"),
        ]
    )
    @allure.title('Проверка, если одного из полей нет, запрос возвращает ошибку и нужно передать в ручку все обязательные поля')
    def test_login_missing_fields(self, login, password, expected_message):
        url = api_client.go_to_url("/api/v1/courier/login")
        payload = {}
        if login is not None:
            payload["login"] = login
        if password is not None:
            payload["password"] = password

        response = requests.post(url, json=payload)

        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}. Тело ответа: {response.text}"
        assert response.json()["message"] == expected_message, f"Ошибка: {response.json()}"


@pytest.mark.parametrize(
    "login, password, expected_message",
    [
        ("invalidlogin", "somepassword", "Учетная запись не найдена"),
        ("validlogin", "wrongpassword", "Учетная запись не найдена"),
        ("invalidlogin", "wrongpassword", "Учетная запись не найдена"),
    ]
)
@allure.title('Проверка, система вернёт ошибку, если неправильно указать логин или пароль и если авторизоваться под несуществующим пользователем, запрос возвращает ошибку')
def test_login_invalid_credentials(login, password, expected_message):
    url = api_client.go_to_url("/api/v1/courier/login")

    payload = {
        "login": login,
        "password": password,
    }

    response = requests.post(url, json=payload)

    assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}. Тело ответа: {response.text}"
    assert response.json()["message"] == expected_message, f"Ошибка: {response.json()}"
