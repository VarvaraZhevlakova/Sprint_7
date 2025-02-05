import allure
import requests
from test.conftest import ApiClient
from urls import base_url_scooter

api_client = ApiClient(base_url_scooter)


class TestGetListOrders:
    @staticmethod
    def get_url(courier_id):
        return api_client.go_to_url(f"/api/v1/orders?courierId={courier_id}")

    @allure.title('Проверка на получение списка заказов по id')
    def test_get_list_orders_scooter(self, login_courier):
        courier_id = login_courier
        url = self.get_url(courier_id)
        response = requests.get(url)

        assert response.status_code == 200, f"Ошибка: статус {response.status_code}. Ответ: {response.text}"
        assert response.json() is not None, f"Курьер с идентификатором {courier_id} не найден"
        assert len({response.text}) > 0, "Ошибка: список заказов пуст"



