import allure
import requests
from requests import Response
from .BaseApiClient import BaseApiClient


class DTPService(BaseApiClient):
    """
        Класс-сервис для работы с эндпоинтом /citysoft/api/v1/dtp.
    """
    DTP_ENDPOINT = "/citysoft/api/v1/dtp"

    def __init__(self, base_url: str, valid_cookie: str):
        """Инициализирует базовые параметры запроса."""
        super().__init__(base_url, valid_cookie, endpoint=self.DTP_ENDPOINT)

    @allure.step("Get DTP data by filters")
    def search_dtp_data_by_filters(self, url_end: str, test_body: dict) -> Response:
        """
            Отправляет POST-запрос для получения ДТП.
        """
        final_url = f"{self.url}{url_end}"
        response = requests.post(final_url,
                                 headers=self.headers, json=test_body)
        return response

    @allure.step("Get DTP data by ID")
    def get_dtp_by_id(self, url_end: str, dtp_id: str) -> Response:
        """
            Отправляет GET-запрос для получения данных о ДТП по ID.
        """
        final_url= f"{self.url}{url_end}{dtp_id}"
        response = requests.get(final_url, headers=self.headers)
        return response

    @allure.step("Check cardId in response is correct")
    def check_dtp_id_in_data(self, response_data: dict, dtp_id: str):
        """
        Проверяет, что ID, возвращенный в теле ответа, совпадает с запрошенным dtp_id.
        """
        returned_id = response_data.get('data', {}).get('cardId')

        assert str(returned_id) == str(dtp_id), \
            (f"Ошибка проверки ID. Запрошен ID: {dtp_id}, "
             f"но в ответе возвращен ID: {returned_id}. "
             f"Полный ответ: {response_data}")

    @allure.step("Check data in response are correct")
    def check_data_in_response(self, response_data: dict, expected_data: str):
        """
        Проверяет, данные возвращенные в теле ответа, совпадают с ожидаемыми
        """
        returned_data = response_data.get("data")

        assert returned_data == expected_data, \
            (f"Ошибка проверки данных. Ожидаем данные содержащие {expected_data}, "
             f"но в ответе: {returned_data}."
             f"Полный ответ: {response_data}")
