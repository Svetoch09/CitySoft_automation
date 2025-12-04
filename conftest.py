import os
import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_environment():
    """
    Автоматически загружает переменные из файла .env в os.environ
    один раз за всю тестовую сессию.
    (autouse=True гарантирует, что это произойдет до любого теста.)
    """
    load_dotenv()
    print("Environment variables loaded from .env")


@pytest.fixture(scope="session")
def base_url() -> str:
    """Предоставляет BASE_URL"""
    base_url = os.getenv("BASE_URL")
    if not base_url:
        pytest.fail("Переменная окружения BASE_URL не установлена.")
    return base_url


@pytest.fixture(scope="session")
def auth_url() -> str:
    """Предоставляет AUTH_URL"""
    auth_url = os.getenv("AUTH_URL")
    if not auth_url:
        pytest.fail("Переменная окружения AUTH_URL не установлена.")
    return auth_url


@pytest.fixture(scope="session")
def user_credentials() -> tuple[str, str]:
    """Фикстура, предоставляющая кортеж (логин, пароль)."""
    login = os.getenv("TEST_LOGIN")
    password = os.getenv("TEST_PASSWORD")

    if not login or not password:
        pytest.fail("Переменные окружения TEST_LOGIN или TEST_PASSWORD не установлены.")
    return login, password  # Возвращаем кортеж (username, password)
