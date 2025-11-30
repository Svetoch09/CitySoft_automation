import allure
import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class MapPage:
    INPUT_LOCATION_LOCATOR = (By.XPATH, '//*[@inputid="on_label"]')
    INPUT_SEARCH_LOCATOR = (By.XPATH, '//*[@type="search"]')
    NOT_FOUND_MESSAGE_XPATH = '//*[contains(text(), " Нет доступных вариантов ")]'

    def __init__(self, driver):
        self.driver = driver
        self.waiter = WebDriverWait(self.driver, 10, 0.5)

    # ----------------------------------------------------------------------

    @allure.step("Input location")
    def input_location(self, location_name: str):
        """
        Кликает по полю ввода локации, очищает поле поиска
        и вводит отформатированный текст.
        После ввода текста список результатов поиска должен быть активен.
        """
        location_field = self.waiter.until(
            EC.visibility_of_element_located(self.INPUT_LOCATION_LOCATOR))
        location_field.click()

        search_field = self.waiter.until(
            EC.visibility_of_element_located(self.INPUT_SEARCH_LOCATOR))

        search_field.clear()
        location_name = location_name.lower().title()
        search_field.send_keys(location_name)

    # ----------------------------------------------------------------------

    @allure.step("Check location")
    def check_location_is_found(self, location_name: str) -> str:
        """
        Проверяет, что в результатах поиска появился хотя бы один элемент,
        содержащий 'location_name'. Получаем результат
        """
        location_name = location_name.lower().title()

        SEARCH_AREA_XPATH = f"//*[contains(@aria-label, '{location_name}')]"
        open_list_btn = f"{SEARCH_AREA_XPATH}/div/button"

        CITY_XPATH = f"//span[text()='{location_name}']"

        try:
            self.waiter.until(
                EC.visibility_of_element_located((By.XPATH, open_list_btn))).click()

            search_result = self.waiter.until(
                EC.visibility_of_element_located((By.XPATH, CITY_XPATH)))
            search_result_text = search_result.text
            search_result.click()

            assert location_name in search_result_text, (
                f"Локация не найдена '{location_name}'")
            logging.info(f"✅ Локация '{location_name}' найдена и кликнута.")
            return "Found and Clicked"

        except TimeoutException:
            logging.error(f"❌ Результаты для '{location_name}' НЕ найдены в течение таймаута.")
            return "Not found"

    # ----------------------------------------------------------------------

    @allure.step("Check non-existing location")
    def check_location_is_not_found(self, location_name: str) -> bool:
        """
            Проверяет, что после ввода несуществующей локации появляется
            сообщение "Нет доступных вариантов".
        """
        location_name = location_name.lower().title()
        try:
            # Используем константу класса
            self.waiter.until(
                EC.visibility_of_element_located((By.XPATH, self.NOT_FOUND_MESSAGE_XPATH))
            )
            logging.info(f"✅ Сообщение 'Нет доступных вариантов' найдено для '{location_name}'.")
            return True

        except TimeoutException:
            logging.error(f"❌ Сообщение 'Нет доступных вариантов' НЕ найдено для '{location_name}'.")
            return False

    @allure.step("Open DTP & AOU menu")
    def open_dtp_aou_menu(self) -> bool:
        DTP_MENU_TITLE_LOCATOR = f"//span[@class='title_text' and text()=' ДТП и АОУ ']"

        try:
            self.waiter.until(
                EC.visibility_of_element_located((By.XPATH, DTP_MENU_TITLE_LOCATOR))
            ).click()
            logging.info(f"✅ Заголовок фильтра 'ДТП и АОУ' найден.")
            return True

        except TimeoutException:
            logging.error(f"❌ Заголовка фильтра 'ДТП и АОУ' не найдено.")
            return False

    @allure.step("Verify DTP & AOU menu is visible")
    def check_dtp_aou_menu_is_visible(self) -> bool:
        """
        Проверяет видимость элементов меню. При неудаче выбрасывает AssertionError
        с детальным сообщением.
        """
        TITLE_DTP_LOCATOR = (By.XPATH, "//*[@class='title' and @for='layerДТП']")
        TITLE_AOU_LOCATOR = (By.XPATH, "//*[@class='title' and @for='layerАварийно-опасные участки']")

        try:
            self.waiter.until(
                EC.visibility_of_element_located(TITLE_DTP_LOCATOR)
            )
            logging.info("✅ Фильтр ДТП (ДТП) виден.")

            try:
                self.waiter.until(
                    EC.visibility_of_element_located(TITLE_AOU_LOCATOR)
                )
                logging.info("✅ Фильтр АОУ (Аварийно-опасные участки) виден.")
                logging.info("✅ Оба фильтра 'ДТП и АОУ' видны. Проверка завершена.")

                return True

            except TimeoutException:
                assert False, "❌ Фильтр 'АОУ' не стал виден в течение таймаута."

        except TimeoutException:
            assert False, "❌ Фильтр 'ДТП' не стал виден в течение таймаута."

    @allure.step("Turn on checkbox")
    def turn_on_checkbox(self, checkbox_locator: tuple[str, str]) -> bool:

        try:
            self.waiter.until(
                EC.element_to_be_clickable(checkbox_locator)
            ).click()
            return True

        except TimeoutException:
            logging.error(f"❌ Чекбокс/радиобаттон не найден.")
            return False

    @allure.step("Check attribute change from False to True")
    def check_attribute_is_true(self, locator: tuple[str, str], attribute_name: str, expected_value: str = 'true'):
        """
        Проверяет, что указанный атрибут элемента принимает ожидаемое строковое значение ('true').
        """
        try:
            self.waiter.until(
                EC.text_to_be_present_in_element_attribute(
                    locator,
                    attribute_name,
                    expected_value
                )
            )
            logging.info(
                f"✅ Атрибут '{attribute_name}' элемента {locator} успешно изменился на '{expected_value}'.")
            return True

        except TimeoutException:
            element = self.driver.find_element(*locator)
            current_value = element.get_attribute(attribute_name)

            error_message = (
                f"❌ ПРОВЕРКА НЕ ПРОШЛА: Атрибут '{attribute_name}' не изменился на '{expected_value}'. "
                f"Текущее значение: '{current_value}'."
            )
            logging.error(error_message)
            assert False, error_message
