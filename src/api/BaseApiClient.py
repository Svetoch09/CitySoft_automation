import requests
import allure
import pytest
from requests import Response


class BaseApiClient:
    """
    Базовый класс для всех API-сервисов. Содержит общую логику:
    инициализацию, заголовки и общие методы проверки ответов.
    """

    def __init__(self, base_url: str, valid_cookie: str, endpoint: str):
        """
        Инициализирует базовые параметры запроса.
        Каждый потомок должен передать свой уникальный 'endpoint'.
        """
        self.url = f"{base_url}{endpoint}"
        self.headers = {
            "Accept": "application/json",
            "Cookie": valid_cookie
        }

    @allure.step("Check status code")
    def check_status_code(self, response: Response, expected_code: int = 200):
        """Проверка статус-код ответа."""
        assert response.status_code == expected_code, \
            f"Ожидался статус {expected_code}, получен {response.status_code}. Ответ: {response.text}"

    @allure.step("Check content type is json")
    def check_content_type_json(self, response: Response):
        """Проверка, что Content-Type - application/json."""
        assert 'application/json' in response.headers.get('Content-Type', ''), \
            "Ответ не содержит 'application/json' в Content-Type."

    @allure.step("Get and validate json body")
    def get_and_validate_json_body(self, response: Response) -> dict:
        """Парсит JSON и проверяет, что это корректный JSON-объект (словарь)."""
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            pytest.fail(f"Ответ не является корректным JSON. Ответ: {response.text}")

        assert isinstance(data, dict), "Тело ответа не является объектом JSON."
        return data

    @allure.step("Check mandatory fields")
    def check_mandatory_fields(self, data: dict, expected_fields: list):
        """Проверка наличия обязательных полей в JSON-ответе."""
        for field in expected_fields:
            assert field in data, f"В ответе JSON отсутствует обязательное поле: '{field}'"

    @allure.step("Check field type is correct")
    def check_field_type(self, data: dict, key: str, expected_type: type):
        """Проверка типов и непустые значений ключевых полей."""
        assert isinstance(data.get(key), expected_type),\
            (f"Поле '{key}' должно быть быть типом {expected_type.__name__}, "
             f"но получено {type(data.get(key)).__name__}.")
