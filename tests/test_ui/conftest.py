import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from src.pages.LoginPage import LoginPage
from src.pages.MapPage import MapPage


@pytest.fixture(scope="session")
def test_location() -> str:
    t_location = os.getenv("TEST_LOCATION")
    if not t_location:
        pytest.fail("Переменная окружения "
                    "TEST_LOCATION не установлена.")
    return t_location


def pytest_addoption(parser) -> None:
    """
        Регистрирует новую опцию командной строки --browser.
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузер для запуска тестов: "
             "'chrome' или 'ff'(firefox)",
    )


@pytest.fixture(scope="function")
def driver(request) -> WebDriver:
    """
    Инициализирует драйвер, считывая имя браузера из командной строки.
    По умолчанию запускает Chrome.
    """
    driver_name = request.config.getoption("--browser").lower()

    if driver_name == "chrome":
        chrome_options = ChromeOptions()
        # chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--guest")
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
        chrome_options.add_experimental_option("prefs", prefs)

        driver_instance = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options,
        )

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
def logged_in_map_page(driver, base_url, user_credentials) -> MapPage:
    """
    Вход в систему через UI(username, password)
    """
    username, password = user_credentials
    login_page = LoginPage(driver, base_url)

    login_page.open()
    login_page.login(username, password)
    login_page.wait_and_check_url(base_url)
    return MapPage(driver, base_url)


@pytest.fixture(scope="function")
def location_selected_map_page(logged_in_map_page, test_location) -> MapPage:
    """
    Выполняет вход, выбирает локацию и возвращает MapPage.
    """
    map_page = logged_in_map_page
    map_page.input_location(test_location)
    map_page.check_location_is_found(test_location)
    return map_page
