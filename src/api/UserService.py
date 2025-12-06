import allure
import requests

from requests import Response
from .BaseApiClient import BaseApiClient


class UserService(BaseApiClient):
    """
        Класс-сервис для работы с эндпоинтом /oauth2/userinfo.
    """

    USER_ENDPOINT = "/oauth2/userinfo"

    def __init__(self, base_url: str, auth_cookie_value: str):
        """
            Инициализирует базовые параметры запроса.
            :param base_url: Базовый URL API.
            :param auth_cookie_value: Значение авторизационной Cookie.
        """
        super().__init__(base_url, auth_cookie_value,
                         endpoint=self.USER_ENDPOINT)

    @allure.step("Get user info")
    def get_user_info(self) -> Response:
        """
            GET-запрос к userinfo и возвращает объект ответа requests.
        """
        response = requests.get(self.url, headers=self.headers)
        return response
