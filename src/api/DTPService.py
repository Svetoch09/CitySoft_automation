import allure
import requests
from requests import Response
from .BaseApiClient import BaseApiClient


class DTPService(BaseApiClient):
    """
        Класс-сервис для работы с эндпоинтом /citysoft/api/v1/dtp.
        Предоставляет методы для получения данных о ДТП по фильтрам
        и по уникальному ID.
    """

    DTP_ENDPOINT = "/citysoft/api/v1/dtp"

    def __init__(self, base_url: str, auth_cookie_value: str):
        """
            Инициализирует базовые параметры запроса.
            :param base_url: Базовый URL API.
            :param auth_cookie_value: Значение авторизационной Cookie.
        """
        super().__init__(base_url, auth_cookie_value,
                         endpoint=self.DTP_ENDPOINT)

    @allure.step("Get DTP data by filters")
    def search_dtp_data_by_filters(self,
                                   url_end: str, test_body: dict) -> Response:
        """
            Отправляет POST-запрос для получения ДТП.
            :param url_end: Окончание URL (например, /all/by_filters).
            :param test_body: Тело запроса (JSON),
            содержащее параметры фильтрации.
        """
        final_url = f"{self.url}{url_end}"
        response = requests.post(final_url,
                                 headers=self.headers, json=test_body)
        return response

    @allure.step("Get DTP data by ID")
    def get_dtp_by_id(self, url_end: str, dtp_id: str) -> Response:
        """
            Отправляет GET-запрос для получения данных о ДТП по ID.
            :param url_end: Окончание URL.
            :param dtp_id: Уникальный ID карточки ДТП.
            :return: Объект ответа requests.Response.
        """
        final_url = f"{self.url}{url_end}{dtp_id}"
        response = requests.get(final_url, headers=self.headers)
        return response

    @allure.step("Check cardId in response is correct")
    def check_dtp_id_in_data(self,
                             response_data: dict, dtp_id: str) -> None:
        """
            Проверяет, что ID, возвращенный в теле ответа,
            совпадает с переданным dtp_id.
            :param response_data: Словарь, содержащий JSON-ответ целиком.
            :param dtp_id: Запрошенный ID (ожидаемое значение).
        """
        returned_id = response_data.get("data", {}).get("cardId")

        assert str(returned_id) == str(dtp_id), (
            f"Ошибка проверки ID. Запрошен ID: {dtp_id}, "
            f"но в ответе возвращен ID: {returned_id}. "
            f"Полный ответ: {response_data}"
        )

    @allure.step("Check data in response are correct")
    def check_data_in_response(self, response_data: dict,
                               expected_data: str) -> None:
        """
            Проверяет, данные возвращенные в теле ответа
            :param response_data: Словарь, содержащий JSON-ответ целиком.
            :param expected_data: Ожидаемое значение поля 'data'.
        """
        returned_data = response_data.get("data")

        assert returned_data == expected_data, (
            f"Ошибка проверки данных. "
            f"Ожидаем данные содержащие {expected_data}, "
            f"но в ответе: {returned_data}."
            f"Полный ответ: {response_data}"
        )
