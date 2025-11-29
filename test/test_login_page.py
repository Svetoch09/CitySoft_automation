import allure
import os
import pytest
from pages.LoginPage import LoginPage

VALID_LOGIN = os.getenv("TEST_LOGIN")
VALID_PASSWORD = os.getenv("TEST_PASSWORD")
INVALID_LOGIN = os.getenv("INVALID_LOGIN")
INVALID_PASSWORD = os.getenv("INVALID_PASSWORD")

NEGATIVE_LOGIN_CASES = [
            # 1. Неверные оба (гарантированно невалидные данные)
            (INVALID_LOGIN, INVALID_PASSWORD, "Ошибка в логине или пароле"),
            # 2. Верный логин, неверный пароль (валидный логин и невалидный пароль)
            (VALID_LOGIN, INVALID_PASSWORD, "Ошибка в логине или пароле"),
            # 3. Неверный логин, верный пароль (невалидный логин и валидный пароль)
            (INVALID_LOGIN, VALID_PASSWORD, "Ошибка в логине или пароле"),
            # 4. Пустой логин
            ("", VALID_PASSWORD, "Ошибка в логине или пароле"),
            # 5. Пустой пароль
            (VALID_LOGIN, "", "Ошибка в логине или пароле"),
        ]

@allure.parent_suite("Login page")
@allure.suite("Login to the system")
@allure.description("Login to the system")
class TestLoginPage:

    @allure.id("Login-1")
    @allure.feature("Вход в систему")
    @allure.title("Успешный вход в систему")
    @allure.description(""" Ввод валидных логина и пароля, вход в систему""")
    @allure.severity("CRITICAL")
    @pytest.mark.positive
    def test_positive_login(self, driver, base_url,user_credentials):
        username, password = user_credentials
        login_page = LoginPage(driver, base_url)
        login_page.open()
        login_page.login(username, password)
        login_page.check_url(base_url)


    @allure.id("Login-2")
    @allure.feature("Вход в систему")
    @allure.title("Негативный вход")
    @allure.description("Проверка входа с невалидными данными")
    @allure.severity("NORMAL")
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
        login_page.check_url(auth_url)
