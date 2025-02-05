import allure
import pytest
import requests

from helpers.gen_input import DataGenerator
from test.conftest import ApiClient
from urls import base_url_scooter

gen = DataGenerator()
api_client = ApiClient(base_url_scooter)


class TestCreateOder:
    @staticmethod
    def get_url():
        return api_client.go_to_url("/api/v1/orders")

    @pytest.mark.parametrize(
        "first_name, last_name, address, metro_station, phone, rent_time, delivery_date, comment, color, expected_status, expected_track",
        [
            (
            gen.generate_first_name(), gen.generate_last_name(), gen.generate_address(), 4, gen.generate_phone_number(),5,
            gen.get_date_plus_days(), gen.generate_comment(), ["BLACK"], 201, True),(
            gen.generate_first_name(), gen.generate_last_name(), gen.generate_address(), 2, gen.generate_phone_number(),10,
            gen.get_date_plus_days(), gen.generate_comment(), ["GREY"], 201, True),(
            gen.generate_first_name(), gen.generate_last_name(), gen.generate_address(), 1, gen.generate_phone_number(),7,
            gen.get_date_plus_days(), gen.generate_comment(), ["BLACK", "GREY"], 201, True),(
            gen.generate_first_name(), gen.generate_last_name(), gen.generate_address(), 5, gen.generate_phone_number(),3,
            gen.get_date_plus_days(), gen.generate_comment(), [], 201, True),(
            gen.generate_first_name(), gen.generate_last_name(), gen.generate_address(), 4, gen.generate_phone_number(),5,
            gen.get_date_plus_days(), gen.generate_comment(), None, 201, True)
        ]
    )
    @allure.title('Проверка на создание успешного заказа')
    def test_create_order_scooter(self, first_name, last_name, address, metro_station, phone, rent_time, delivery_date, comment, color, expected_status, expected_track, cancel_order):
        url = self.get_url()

        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "address": address,
            "metroStation": metro_station,
            "phone": phone,
            "rentTime": rent_time,
            "deliveryDate": delivery_date,
            "comment": comment,
            "color": color if color is not None else []
        }

        response = requests.post(url, json=payload)

        assert response.status_code == 201, f"Ожидался статус 201 Created, но получен {response.status_code}. Тело ответа: {response.text}"

        if expected_track:
            response_json = response.json()
            assert "track" in response_json, f"Ошибка: в ответе отсутствует поле 'track'. Ответ: {response_json}"
            track_id = response_json.get("track")
            cancel_order(track_id)

