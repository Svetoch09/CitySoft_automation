import allure
import pytest
from pages.LoginPage import LoginPage
from data.login_data import NEGATIVE_LOGIN_CASES


@allure.parent_suite("UI tests")
@allure.suite("Login to the system")
@allure.description("Login to the system")
class TestLoginPage:

    @allure.id("Login-1")
    @allure.feature("Вход в систему")
    @allure.title("Успешный вход в систему")
    @allure.description(""" Ввод валидных логина и пароля, вход в систему""")
    @allure.severity("BLOCKER")
    @pytest.mark.positive
    def test_positive_login(self, driver, map_url, user_credentials):
        username, password = user_credentials
        login_page = LoginPage(driver, map_url)
        login_page.open()
        login_page.login(username, password)
        login_page.wait_and_check_url(map_url)

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
    def test_negative_login(self, driver, map_url, auth_url, username_input,
                            password_input, description):
        login_page = LoginPage(driver, map_url)
        login_page.open()
        login_page.login(username_input, password_input)
        actual_msg = login_page.get_error_message_text()
        login_page.check_error_msg(actual_msg)
        login_page.wait_and_check_url(auth_url)
