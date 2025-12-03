import os

import pytest
from src.api.DTPService import DTPService
from src.api.UserService import UserService
from copy import deepcopy # для безопасной копии словаря
from data.api_dtp_data import DTP_FILTER_BASE_BODY


@pytest.fixture(scope="session")
def valid_cookie():
    """Фикстура для VALID_COOKIE_VALUE."""
    cookie = os.getenv("VALID_COOKIE_VALUE")
    if not cookie:
        pytest.fail("Переменная VALID_COOKIE_VALUE не найдена в .env")
    return cookie

@pytest.fixture(scope="function")
def user_service(base_url, valid_cookie):
    """
    Фикстура создает экземпляр нашего сервисного класса
    для каждого тестового метода.
    """
    return UserService(base_url, valid_cookie)

@pytest.fixture(scope="function")
def map_service(base_url, valid_cookie):
    """
    Фикстура создает экземпляр нашего сервисного класса
    для каждого тестового метода.
    """
    return DTPService(base_url, valid_cookie)

@pytest.fixture(scope="function")
def dtp_base_body():
    """Возвращает глубокую копию базового тела запроса DTP."""
    return deepcopy(DTP_FILTER_BASE_BODY)
