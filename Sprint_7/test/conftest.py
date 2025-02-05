import pytest
import requests
from helpers.gen_input import DataGenerator
from urls import base_url_scooter


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def go_to_url(self, endpoint):
        return f"{self.base_url}{endpoint}"


gen = DataGenerator()
api_client = ApiClient(base_url_scooter)


@pytest.fixture
def create_courier(): # Фикстура для создания курьера перед тестами
    url = api_client.go_to_url("/api/v1/courier")

    payload = {
        "login": gen.generate_login(),
        "password": gen.generate_password(),
        "firstName": gen.generate_first_name()
    }

    response = requests.post(url, json=payload)

    return response, payload


@pytest.fixture
def delete_courier(): # Фикстура для удаления курьера по ID после тестов

    def delete(courier_id):
        url = api_client.go_to_url(f"/api/v1/courier/{courier_id}")
        response = requests.delete(url)
        return response

    return delete


@pytest.fixture
def login_courier(create_courier): # Фикстура логина созданного курьера
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
    return response_json.get("id")

@pytest.fixture
def cancel_order(): # Фикстура для отмены заказа по track"
    def cancel(track_id):
        url = api_client.go_to_url(f"/api/v1/orders/cancel")
        payload = {"track": track_id}

        response = requests.put(url, json=payload)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            return response.json()
        else:
            return None

    return cancel











