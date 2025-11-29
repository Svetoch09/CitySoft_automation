import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.LoginPage import LoginPage
from pages.MapPage import MapPage

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
AUTH_URL = os.getenv("AUTH_URL_BASE")


@pytest.fixture(scope="session")
def base_url() -> str:
    if not BASE_URL:
        pytest.fail("Переменная окружения BASE_URL не установлена.")
    return BASE_URL


@pytest.fixture(scope="session")
def auth_url() -> str:
    if not AUTH_URL:
        pytest.fail("Переменная окружения AUTH_URL_BASE не установлена.")
    return AUTH_URL


@pytest.fixture(scope="session")
def user_credentials() -> tuple[str, str]:
    """Фикстура, предоставляющая кортеж (логин, пароль)."""
    login = os.getenv("TEST_LOGIN")
    password = os.getenv("TEST_PASSWORD")

    if not login or not password:
        pytest.fail("Переменные окружения TEST_LOGIN или TEST_PASSWORD не установлены.")
    return login, password  # Возвращаем кортеж (username, password)


def pytest_addoption(parser) -> None:
    """Регистрирует новую опцию командной строки --browser."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",  # <-- Значение по умолчанию
        help="Браузер для запуска тестов: 'chrome' или 'ff'(firefox)"
    )


@pytest.fixture(scope="function")
def driver(request) -> WebDriver:
    """
    Инициализирует драйвер, считывая имя браузера из командной строки.
    По умолчанию запускает Chrome.
    """
    # Получаем имя браузера из опции --browser
    driver_name = request.config.getoption("--browser").lower()

    # Логика инициализации
    if driver_name == "chrome":
        chrome_options = ChromeOptions()

        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--guest")
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        chrome_options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options)
    elif driver_name == "ff" or driver_name == "firefox":
        firefox_options = FirefoxOptions()  # pytest --browser=ff
        firefox_options.set_preference("signon.rememberSignons", False)
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=firefox_options)
    else:
        raise ValueError(f"Браузер '{driver_name}' не поддерживается.")

    # Общие настройки
    driver.maximize_window()
    driver.implicitly_wait(5)

    # Возврат драйвера и Teardown
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def logged_in_map_page(driver, base_url, user_credentials) -> MapPage:
    """
    Вход в систему, переходит на MapPage и возвращает
    экземпляр MapPage, готовый к тестированию.
    Зависит от фиксатур: driver, base_url, user_credentials.
    """
    username, password = user_credentials
    login_page = LoginPage(driver, base_url)
    login_page.open()
    login_page.login(username, password)
    return MapPage(driver)


@pytest.fixture(scope="function")
def location_selected_map_page(logged_in_map_page) -> MapPage:
    """
        Выполняет вход, выбирает локацию и возвращает MapPage.
    """
    location_for_tests = "Казань"

    map_page = logged_in_map_page
    map_page.input_location(location_for_tests)
    map_page.check_location_is_found(location_for_tests)
    return map_page
