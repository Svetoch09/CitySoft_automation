import logging

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data.ui_map_page_locators import (
    LOGOUT_BUTTON,
    LOGIN_HEADER,
    INPUT_LOCATION_FIELD,
    INPUT_SEARCH_FIELD,
    NOT_FOUND_MESSAGE,
    DTP_AOU_MENU_TITLE,
    DTP_FILTER_TITLE,
    AOU_FILTER_TITLE,
)


class MapPage:
    """
        Page Object для страницы карты.
        Содержит методы для управления сессией,
        поиска локации и работы с фильтрами ДТП/АОУ.
    """

    def __init__(self, driver, base_app_url: str):
        """
            Инициализирует Page Object.
            :param driver: Экземпляр WebDriver.
            :param base_app_url: Базовый URL страницы приложения (карты).
        """
        self.driver = driver
        self.base_app_url = base_app_url
        self.waiter = WebDriverWait(self.driver, 10, 0.5)

    @allure.step(
        "Click the 'Logout' button and confirm "
        "the transition to the login page."
    )
    def logout_and_verify(self) -> "MapPage":
        """
            Выполняет выход из учетной записи и
            проверку перехода на страницу авторизации
        """
        expected_text = "Добро пожаловать в СитиСофт"
        exit_btn = self.waiter.until(EC.element_to_be_clickable(LOGOUT_BUTTON))
        exit_btn.click()

        try:
            header = self.waiter.until(
                EC.visibility_of_element_located(LOGIN_HEADER))
            raw_text = header.text
            cleaned_text = " ".join(
                raw_text.replace("\n", " ").replace(
                    "\xa0", " ").strip().split()
            )
            assert cleaned_text == expected_text, (
                f"❌ Текст заголовка не совпадает. "
                f"Ожидалось '{expected_text}' внутри текста. "
                f"Фактический очищенный текст: '{cleaned_text}'"
            )

            logging.info(
                "✅ Успешное разлогинивание: "
                "заголовок 'Добро пожаловать в СитиСофт' найден."
            )

        except TimeoutException:
            current_url = self.driver.current_url
            raise AssertionError(
                f"❌ Разлогинивание не завершено."
                f"Заголовок страницы входа не появился за отведенное время. "
                f"Текущий URL: {current_url}"
            )
        return self

    @allure.step("Input location")
    def input_location(self, location_name: str) -> None:
        """
            Кликает по полю ввода локации, очищает поле поиска
            и вводит отформатированный текст.
            После ввода текста список результатов поиска должен быть активен.
            :param location_name: Название локации для поиска.
        """
        location_field = self.waiter.until(
            EC.visibility_of_element_located(INPUT_LOCATION_FIELD)
        )
        location_field.click()

        search_field = self.waiter.until(
            EC.visibility_of_element_located(INPUT_SEARCH_FIELD)
        )

        search_field.clear()
        location_name = location_name.lower().title()
        search_field.send_keys(location_name)


    @allure.step("Check location is found")
    def check_location_is_found(self, location_name: str) -> str:
        """
            Проверяет, что в результатах поиска появился хотя бы один элемент,
            содержащий 'location_name'. Получаем результат
            :param location_name: Название локации для поиска.
        """
        location_name = location_name.lower().title()
        search_area_locator = f"//*[contains(@aria-label, '{location_name}')]"
        open_list_btn = f"{search_area_locator}/div/button"
        city_locator = f"//span[text()='{location_name}']"

        try:
            self.waiter.until(
                EC.visibility_of_element_located((By.XPATH, open_list_btn))
            ).click()

            search_result = self.waiter.until(
                EC.visibility_of_element_located((By.XPATH, city_locator))
            )
            search_result_text = search_result.text
            search_result.click()

            assert (
                location_name in search_result_text
            ), f"Локация не найдена '{location_name}'"
            logging.info(
                f"✅ Локация '{location_name}' найдена и кликнута.")
            return "Found and Clicked"

        except TimeoutException:
            logging.error(
                f"❌ Результаты для '{location_name}'"
                f" НЕ найдены в течение таймаута."
            )
            return "Not found"


    @allure.step("Check non-existing location is not found")
    def check_location_is_not_found(self,
                                    location_name: str) -> bool:
        """
        Проверяет, что после ввода несуществующей локации появляется
        сообщение "Нет доступных вариантов".
        :param location_name: Несуществующая локация.
        """
        location_name = location_name.lower().title()
        try:
            self.waiter.until(
                EC.visibility_of_element_located((NOT_FOUND_MESSAGE)))
            logging.info(
                f"✅ Сообщение "
                f"'Нет доступных вариантов' найдено для '{location_name}'."
            )
            return True

        except TimeoutException:
            logging.error(
                f"❌ Сообщение "
                f"'Нет доступных вариантов' НЕ найдено для '{location_name}'."
            )
            return False

    @allure.step("Open DTP & AOU menu")
    def open_dtp_aou_menu(self) -> bool:
        """
            Кликает по заголовку 'ДТП и АОУ' для открытия меню фильтров.
        """

        try:
            self.waiter.until(
                EC.visibility_of_element_located(DTP_AOU_MENU_TITLE)
            ).click()
            logging.info("✅ Заголовок фильтра 'ДТП и АОУ' найден.")
            return True

        except TimeoutException:
            logging.error("❌ Заголовка фильтра 'ДТП и АОУ' не найдено.")
            return False

    @allure.step("Verify DTP & AOU menu is visible")
    def check_dtp_aou_menu_is_visible(self) -> bool:
        """
            Проверяет видимость ключевых элементов
            внутри меню фильтров (ДТП и АОУ).
        """

        try:
            self.waiter.until(
                EC.visibility_of_element_located(DTP_FILTER_TITLE))
            logging.info("✅ Фильтр ДТП виден.")

            self.waiter.until(
                EC.visibility_of_element_located(AOU_FILTER_TITLE))
            logging.info("✅ Фильтр АОУ виден.")

            return True

        except TimeoutException:
            raise AssertionError(
                "❌ Не удалось найти один "
                "или оба ключевых элемента меню фильтров."
            )

    @allure.step("Turn on checkbox/radio button")
    def turn_on_checkbox(self,
                         checkbox_locator: tuple[str, str]) -> bool:
        """
            Кликает по чекбоксу или радиобаттону.
            :param checkbox_locator: Локатор элемента.
        """
        try:
            self.waiter.until(
                EC.element_to_be_clickable(checkbox_locator)).click()
            return True

        except TimeoutException:
            logging.error("❌ Чекбокс/радиобаттон не найден.")
            return False

    @allure.step("Check attribute change from False to True")
    def check_attribute_is_true(
        self,
        locator: tuple[str, str],
        attribute_name: str,
        expected_value: str = "true",
    ):
        """
            Проверяет, что указанный атрибут элемента принимает
            ожидаемое строковое значение ('true').
            :param locator: Локатор проверяемого элемента.
            :param attribute_name: Имя атрибута для проверки.
            :param expected_value: Ожидаемое строковое значение ('true').
        """
        try:
            self.waiter.until(
                EC.text_to_be_present_in_element_attribute(
                    locator, attribute_name, expected_value
                )
            )
            logging.info(
                f"✅ Атрибут '{attribute_name}' элемента {locator} "
                f"успешно изменился на '{expected_value}'."
            )
            return True

        except TimeoutException:
            element = self.driver.find_element(*locator)
            current_value = element.get_attribute(attribute_name)

            error_message = (
                f"❌ ПРОВЕРКА НЕ ПРОШЛА: Атрибут '{attribute_name}' "
                f"не изменился на '{expected_value}'. "
                f"Текущее значение: '{current_value}'."
            )
            logging.error(error_message)
            assert False, error_message
