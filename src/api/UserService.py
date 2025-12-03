import allure
import requests

from requests import Response
from .BaseApiClient import BaseApiClient


class UserService(BaseApiClient):
    """
    Класс-сервис для работы с эндпоинтом /oauth2/userinfo.
    """
    USER_ENDPOINT = "/oauth2/userinfo"

    def __init__(self, base_url: str, valid_cookie: str):
        """Инициализирует базовые параметры запроса."""
        super().__init__(base_url, valid_cookie, endpoint=self.USER_ENDPOINT)

    @allure.step("Get user info")
    def get_user_info(self) -> Response:
        """GET-запрос к userinfo и возвращает объект ответа requests."""
        response = requests.get(self.url, headers=self.headers)
        return response