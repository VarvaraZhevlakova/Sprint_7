import allure
import pytest
import requests

from helpers.gen_input import DataGenerator
from test.conftest import ApiClient
from urls import base_url_scooter

gen = DataGenerator()
api_client = ApiClient(base_url_scooter)


class TestCourier:

    @staticmethod
    def get_url():
        return api_client.go_to_url("/api/v1/courier")

    @allure.title('Проверка, что курьер успешно создан')
    def test_create_courier(self, create_courier, login_courier, delete_courier):
        response, payload = create_courier
        assert response.status_code == 201, f"Ошибка при создании курьера: {response.status_code}, тело ответа: {response.text}"
        expected_response = {"ok": True}
        assert response.json() == expected_response, f"Ошибка: ответ {response.json()} не соответствует {expected_response}"

        courier_id = login_courier
        delete_courier(courier_id)

    @allure.title('Проверка, что нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier(self,create_courier, login_courier, delete_courier):
        url = self.get_url()
        response_1, payload = create_courier
        assert response_1.status_code == 201, f"Ошибка при создании курьера: {response_1.status_code}, тело ответа: {response_1.text}"

        response_2 = requests.post(url, json=payload)

        assert response_2.status_code == 409, f"Ошибка: {response_2.status_code}, тело ответа: {response_2.text}"
        assert response_2.json().get("message") == "Этот логин уже используется. Попробуйте другой."
        courier_id = login_courier
        delete_courier(courier_id)

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title('Проверка, чтобы создать курьера, нужно передать в ручку все обязательные поля')
    def test_create_courier_missing_field(self, create_courier, missing_field, login_courier, delete_courier):
        url = self.get_url()
        response, payload = create_courier
        del payload[missing_field]
        response = requests.post(url, json=payload)

        assert response.status_code == 400, f"Ошибка: {response.status_code}, тело ответа: {response.text}"
        expected_message = "Недостаточно данных для создания учетной записи"
        response_data = response.json()
        assert response_data.get("message") == expected_message, f"Некорректное сообщение ошибки: {response_data}"
        courier_id = login_courier
        delete_courier(courier_id)






