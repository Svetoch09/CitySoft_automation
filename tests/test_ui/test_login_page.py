import allure
import pytest
from typing import Tuple, List, Union

from selenium.webdriver.remote.webdriver import WebDriver
from src.pages.LoginPage import LoginPage
from data.ui_login_data import NEGATIVE_LOGIN_CASES


@allure.parent_suite("UI tests")
@allure.suite("Login to the system")
@allure.description("Login to the system")
@pytest.mark.ui
class TestLoginPage:

    @allure.id("Login-1")
    @allure.feature("Вход в систему")
    @allure.title("Успешный вход в систему")
    @allure.description(""" Ввод валидных логина и пароля, вход в систему""")
    @allure.severity("BLOCKER")
    @pytest.mark.positive
    def test_positive_login(
            self,
            driver: WebDriver,
            base_url: str,
            user_credentials: Tuple[str, str]) -> None:
        """
            Тест: успешный вход в систему с валидной авторизацией.
            :param driver: Экземпляр WebDriver.
            :param base_url: Базовый URL целевого приложения.
            :param user_credentials: Кортеж (логин, пароль) валидного пользователя.
            :return: None
        """
        username, password = user_credentials
        login_page = LoginPage(driver, base_url)
        login_page.open()
        login_page.login(username, password)
        login_page.wait_and_check_url(base_url)

    @allure.id("Login-2")
    @allure.feature("Вход в систему")
    @allure.title("Негативный вход")
    @allure.description("Проверка входа с невалидными данными")
    @allure.severity("BLOCKER")
    @pytest.mark.parametrize(
        "username_input, password_input, description", NEGATIVE_LOGIN_CASES
    )
    @pytest.mark.negative
    def test_negative_login(
        self,
        driver: WebDriver,
        base_url: str,
        auth_url: str,
        username_input: str,
        password_input: str,
        description) -> None:
        """
            Проверка входа в систему с невалидными или отсутствующими учетными данными.
            :param driver: Экземпляр WebDriver.
            :param base_url: URL целевого приложения.
            :param auth_url: URL страницы авторизации.
            :param username_input: Тестовое значение логина.
            :param password_input: Тестовое значение пароля.
        """
        login_page = LoginPage(driver, base_url)
        login_page.open()
        login_page.login(username_input, password_input)
        actual_msg = login_page.get_error_message_text()
        login_page.check_error_msg(actual_msg)
        login_page.wait_and_check_url(auth_url)
