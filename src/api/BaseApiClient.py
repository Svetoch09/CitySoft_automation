import requests
import allure
import pytest
from requests import Response


class BaseApiClient:
    """
        Базовый класс для всех API-сервисов.
        Содержит общую логику:
        инициализацию, заголовки и общие методы проверки ответов.
    """

    def __init__(self, base_url: str, auth_cookie_value: str,
                 endpoint: str):
        """
            Инициализирует базовые параметры запроса.
            :param base_url: Базовый URL API.
            :param auth_cookie_value: Значение авторизационной Cookie.
            :param endpoint: Уникальное окончание URL для сервиса
        """
        self.url = f"{base_url}{endpoint}"
        self.headers = {
            "Accept": "application/json",
            "Cookie": f"_oauth2_proxy_map={auth_cookie_value}",
        }

    @allure.step("Check status code")
    def check_status_code(self, response: Response,
                          expected_code: int = 200) -> None:
        """
            Проверка статус-код ответа.
            :param response: Объект ответа requests.Response.
            :param expected_code: Ожидаемый код HTTP.
            По умолчанию 200.

        """
        assert (response.status_code == expected_code), \
            (f"Ожидался статус {expected_code}, "
             f"получен {response.status_code}. Ответ: {response.text}")

    @allure.step("Check content type is json")
    def check_content_type_json(self, response: Response) -> None:
        """
            Проверка, что Content-Type - application/json.
            :param response: Объект ответа requests.Response.
        """
        assert "application/json" in response.headers.get(
            "Content-Type", ""
        ), "Ответ не содержит 'application/json' в Content-Type."

    @allure.step("Get and validate json body")
    def get_and_validate_json_body(self, response: Response) -> dict:
        """
            Парсит JSON и проверяет, что
            это корректный JSON-объект (словарь).
            :param response: Объект ответа requests.Response.
        """
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            pytest.fail(f"Ответ не является корректным JSON."
                        f" Ответ: {response.text}")

        assert isinstance(data, dict), "Тело ответа не является объектом JSON."
        return data

    @allure.step("Check mandatory fields")
    def check_mandatory_fields(self, data: dict,
                               expected_fields: list) -> None:
        """
            Проверка наличия обязательных полей в JSON-ответе.
            :param data: Словарь, полученный из JSON-ответа.
            :param expected_fields: Список обязательных строковых ключей.
        """
        for field in expected_fields:
            assert (field in data), \
                f"В ответе JSON отсутствует обязательное поле: '{field}'"

    @allure.step("Check field type is correct")
    def check_field_type(self, data: dict, key: str,
                         expected_type: type) -> None:
        """
            Проверка типов и непустые значений ключевых полей.
            :param data: Словарь, содержащий данные ответа.
            :param key: Имя проверяемого поля.
            :param expected_type: Ожидаемый тип.
        """
        assert isinstance(data.get(key), expected_type), (
            f"Поле '{key}' должно быть быть типом {expected_type.__name__}, "
            f"но получено {type(data.get(key)).__name__}."
        )
