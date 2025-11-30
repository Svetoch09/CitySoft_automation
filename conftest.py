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


@pytest.fixture(scope="session")
def map_url() -> str:
    m_url = os.getenv("BASE_URL")
    if not m_url:
        pytest.fail("Переменная окружения BASE_URL не установлена.")
    return m_url


@pytest.fixture(scope="session")
def auth_url() -> str:
    a_url = os.getenv("AUTH_URL")
    if not a_url:
        pytest.fail("Переменная окружения AUTH_URL не установлена.")
    return a_url


@pytest.fixture(scope="session")
def test_location() -> str:
    t_location = os.getenv("TEST_LOCATION")
    if not t_location:
        pytest.fail("Переменная окружения TEST_LOCATION не установлена.")
    return t_location


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

    if driver_name == "chrome":
        chrome_options = ChromeOptions()
        #chrome_options.add_argument("--headless=new")
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

        driver_instance = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options)

    elif driver_name in ["ff", "firefox"]:
        ff_options = FirefoxOptions()  # pytest --browser=ff
        # ff_options.add_argument("-headless")
        ff_options.set_preference("signon.rememberSignons", False)
        driver_instance = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=ff_options)
    else:
        raise ValueError(f"Браузер '{driver_name}' не поддерживается.")

    driver_instance.maximize_window()
    driver_instance.implicitly_wait(5)

    yield driver_instance
    driver_instance.quit()


@pytest.fixture(scope="function")
def logged_in_map_page(driver, map_url, user_credentials) -> MapPage:
    """
    Вход в систему, переходит на MapPage и возвращает
    экземпляр MapPage, готовый к тестированию.
    Зависит от фиксатур: driver, base_url, user_credentials.
    """
    username, password = user_credentials
    login_page = LoginPage(driver, map_url)
    login_page.open()
    login_page.login(username, password)
    login_page.wait_and_check_url(map_url)
    return MapPage(driver, map_url)


@pytest.fixture(scope="function")
def location_selected_map_page(logged_in_map_page, test_location) -> MapPage:
    """
        Выполняет вход, выбирает локацию и возвращает MapPage.
    """
    map_page = logged_in_map_page
    map_page.input_location(test_location)
    map_page.check_location_is_found(test_location)
    return map_page
