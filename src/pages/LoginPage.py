import logging

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data.ui_login_page_locators import (
    INPUT_USERNAME_FIELD,
    INPUT_PASSWORD_FIELD,
    LOGIN_BUTTON,
    ERROR_MESSAGE_CONTAINER,
)


class LoginPage:

    def __init__(self, driver, base_url):
        """
            Инициализирует Page Object.
            :param driver: Экземпляр WebDriver.
            :param base_url: Базовый URL страницы авторизации.
        """
        self.driver = driver
        self.base_url = base_url
        self.waiter = WebDriverWait(self.driver, 10, 0.5)

    @allure.step("Open login page")
    def open(self) -> None:
        """
            Открывает страницу логина по заданному базовому URL.
        """
        self.driver.get(self.base_url)

    @allure.step("Login with creds username= LOGIN and "
                 "password = PASSWORD")
    def login(self, username, password) -> None:
        """
            Выполняет вход в систему, вводя учетные данные
            и нажимая кнопку "Вход".
            :param username: Логин пользователя.
            :param password: Пароль пользователя.
        """
        user_name_field = self.waiter.until(
            EC.visibility_of_element_located(INPUT_USERNAME_FIELD)
        )
        user_name_field.clear()
        user_name_field.send_keys(username)

        password_field = self.waiter.until(
            EC.visibility_of_element_located(INPUT_PASSWORD_FIELD)
        )
        password_field.clear()
        password_field.send_keys(password)

        login_btn = self.waiter.until(
            EC.visibility_of_element_located(LOGIN_BUTTON))
        login_btn.click()

    @allure.step("Wait until url has changed")
    def wait_and_check_url(self, expected_prefix: str) -> bool:
        """
            Ждет, пока текущий URL не будет содержать ожидаемый префикс,
            а затем выполняет строгую проверку startswith.
            :param expected_prefix: Ожидаемый префикс URL.
        """
        try:
            self.waiter.until(EC.url_contains(expected_prefix))
            actual_url = self.driver.current_url
            assert actual_url.startswith(expected_prefix), (
                f"❌ Ошибка URL. "
                f"Ожидался URL, начинающийся с '{expected_prefix}', "
                f"но фактический URL: '{actual_url}'"
            )
            logging.info(f"✅ URL успешно проверен. Текущий URL: {actual_url}")
            return True

        except TimeoutException:
            current_url = self.driver.current_url
            raise AssertionError(
                f"❌ Timeout! "
                f"URL не изменился на {expected_prefix} за отведенное время. "
                f"Текущий URL: {current_url}"
            )

    @allure.step("Check for error message")
    def get_error_message_text(self) -> str:
        """
            Получает текст ошибки, который отображается на странице
            не как обычный HTML-текст,
            а как CSS-псевдоэлемент (::before).
        """
        JS_GET_CONTENT = (
            "return window.getComputedStyle(arguments[0], '::before')."
            "getPropertyValue('content');"
        )
        try:
            error_container = self.waiter.until(
                EC.presence_of_element_located(ERROR_MESSAGE_CONTAINER)
            )

            content = self.driver.execute_script(
                JS_GET_CONTENT, error_container)
            return content

        except TimeoutException:
            return ""
        except Exception as e:
            print(f"Ошибка при чтении текста ошибки из ::before: {e}")
            return ""

    @allure.step("Check error msg = expected msg")
    def check_error_msg(self, actual_msg: str) -> None:
        """
            Проверяет, что текст полученного сообщения
            об ошибке соответствует ожидаемому.
            :param actual_msg: Фактически полученный текст ошибки.
        """
        expected_msg = "Ошибка в логине или пароле"
        assert expected_msg in actual_msg, (
            f"Ожидалась ошибка '{expected_msg}', "
            f"но получено сообщение: '{actual_msg}'"
        )
