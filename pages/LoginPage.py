import allure
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class LoginPage:
    INPUT_USERNAME_LOCATOR = (By.ID, "username")
    INPUT_PASSWORD_LOCATOR = (By.ID, "password")
    LOGIN_BTN_LOCATOR = (By.ID, "kc-login")
    ERROR_CONTAINER_LOCATOR = (By.ID, "input-error")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.waiter = WebDriverWait(self.driver, 10, 0.5)

    @allure.step("Open login page")
    def open(self) -> None:
        self.driver.get(self.base_url)

    @allure.step("Login with creds username= LOGIN and "
                 "password = PASSWORD")
    def login(self, username, password) -> None:
        user_name_field = self.waiter.until(
            EC.visibility_of_element_located(self.INPUT_USERNAME_LOCATOR))
        user_name_field.clear()
        user_name_field.send_keys(username)

        password_field = self.waiter.until(
            EC.visibility_of_element_located(self.INPUT_PASSWORD_LOCATOR))
        password_field.clear()
        password_field.send_keys(password)

        login_btn = self.waiter.until(
            EC.visibility_of_element_located(self.LOGIN_BTN_LOCATOR))
        login_btn.click()

    @allure.step("Check current url = expected url")
    def check_url(self, url: str):
        actual_url = self.driver.current_url
        assert actual_url.startswith(url), (
            f"Ожидался URL ({url}), "
            f"но фактический URL: {actual_url}"
        )
        logging.info(f"✅ URL успешно проверен. Текущий URL: {actual_url}")

    @allure.step("Check for error message")
    def get_error_message_text(self) -> str:
        """ Получает текст ошибки, который отображается на странице не как обычный HTML-текст,
            а как CSS-псевдоэлемент (::before)."""
        JS_GET_CONTENT = ("return window.getComputedStyle(arguments[0], '::before')."
                          "getPropertyValue('content');")
        try:
            # 1. Ожидаем появления самого родительского элемента по его ID
            error_container = self.waiter.until(
                EC.presence_of_element_located(self.ERROR_CONTAINER_LOCATOR))

            # 2. Выполняем JavaScript для чтения содержимого ::before
            # Результат возвращается в переменной content
            content = self.driver.execute_script(JS_GET_CONTENT, error_container)
            return content

        except TimeoutException:  # Если родительский элемент не появился за 10 секунд
            return ""
        except Exception as e:
            # Общий обработчик ошибок
            print(f"Ошибка при чтении текста ошибки из ::before: {e}")
            return ""

    @allure.step("Check error msg = expected msg")
    def check_error_msg(self, actual_msg: str):
        expected_msg = "Ошибка в логине или пароле"
        assert expected_msg in actual_msg, (
            f"Ожидалась ошибка '{expected_msg}', "
            f"но получено сообщение: '{actual_msg}'"
        )
