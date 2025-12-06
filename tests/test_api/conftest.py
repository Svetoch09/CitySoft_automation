import pytest
from selenium import webdriver
from src.api.DTPService import DTPService
from src.api.UserService import UserService
from copy import deepcopy
from data.api_dtp_data import DTP_FILTER_BASE_BODY
from src.pages.LoginPage import LoginPage


@pytest.fixture(scope="session")
def session_driver(request):
    """
        Инициализирует и закрывает драйвер
        ТОЛЬКО ОДИН РАЗ за сессию
        для авторизации.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver_instance = webdriver.Chrome(options=options)

    driver_instance.implicitly_wait(5)

    yield driver_instance
    driver_instance.quit()


@pytest.fixture(scope="session")
def auth_cookie_value(session_driver, base_url, user_credentials):
    """
        Выполняет полный UI-вход в систему один раз за сессию и
        возвращает значение авторизационной куки.
    """
    username, password = user_credentials
    login_page = LoginPage(session_driver, base_url)
    login_page.open()
    login_page.login(username, password)

    try:
        login_page.wait_and_check_url(base_url)
        print(f"URL после логина: {session_driver.current_url}")
    except Exception:
        pytest.fail("UI-авторизация не удалась: "
                    "не произошел редирект на целевой URL.")

    cookie = session_driver.get_cookie("_oauth2_proxy_map")

    if cookie and "value" in cookie:
        return cookie["value"]
    pytest.fail(
        "UI-авторизация успешна, "
        "но не удалось извлечь cookie '_oauth2_proxy_map'."
    )


@pytest.fixture(scope="function")
def user_service(base_url, auth_cookie_value):
    """
        Создает экземпляр user-сервисного класса
        для каждого тестового метода.
    """
    return UserService(base_url, auth_cookie_value)


@pytest.fixture(scope="function")
def map_service(base_url, auth_cookie_value):
    """
        Создает экземпляр map-сервисного класса
        для каждого тестового метода.
    """
    return DTPService(base_url, auth_cookie_value)


@pytest.fixture(scope="function")
def dtp_base_body():
    """
        Возвращает глубокую копию
        базового тела запроса ДТП.
    """
    return deepcopy(DTP_FILTER_BASE_BODY)
