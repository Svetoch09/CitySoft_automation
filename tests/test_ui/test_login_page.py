import allure
import pytest

from data.ui_login_data import NEGATIVE_LOGIN_CASES
from src.pages.LoginPage import LoginPage


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
    def test_positive_login(self, driver, base_url, user_credentials):
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
        "username_input, password_input, description",
        NEGATIVE_LOGIN_CASES
    )
    @pytest.mark.negative
    def test_negative_login(self, driver, base_url, auth_url, username_input,
                            password_input, description):
        login_page = LoginPage(driver, base_url)
        login_page.open()
        login_page.login(username_input, password_input)
        actual_msg = login_page.get_error_message_text()
        login_page.check_error_msg(actual_msg)
        login_page.wait_and_check_url(auth_url)
