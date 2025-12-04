import allure
import pytest
from typing import List, Dict, Any, Union, Tuple
from data.ui_checkbox_data import ALL_CHECKBOX_DATA

from src.pages.MapPage import MapPage

ALL_MAIN_CHECKBOXES = list(ALL_CHECKBOX_DATA.keys())
DTP_CHILDREN_CHECKBOXES = ALL_CHECKBOX_DATA["DTP"]["children"]
AOU_CHILDREN_RADIO = ALL_CHECKBOX_DATA["AOU"]["children"]


@allure.parent_suite("UI tests")
@allure.suite("Map page")
@allure.description("Work with map page")
@pytest.mark.ui
class TestMapPage:
    """
        Класс для проверки функциональности
        страницы карты (Map Page).
    """

    @allure.id("Map-1")
    @allure.feature("Выход из учетной записи")
    @allure.title("Проверка функциональности разлогинивания")
    @allure.description(
        """ Нажатие на кнопку выхода и проверка
            что переходим на страницу авторизации""")
    @allure.severity("CRITICAL")
    @pytest.mark.positive
    def test_successful_logout(self, logged_in_map_page: MapPage) -> None:
        """
            Проверка выхода из системы и успешного
            перехода на страницу авторизации.
            :param logged_in_map_page: Фикстура авторизованной MapPage.
        """
        map_page = logged_in_map_page
        map_page.logout_and_verify()

    @allure.id("Map-2")
    @allure.feature("Поиск локации")
    @allure.title("Поиск существующей локации")
    @allure.description(
        """ Ввод локации в поле поиска и
            проверка успешного выполнения поиска""")
    @allure.severity("CRITICAL")
    @pytest.mark.parametrize("location", ["Нижний Новгород"])
    @pytest.mark.positive
    def test_find_location(self, logged_in_map_page: MapPage,
                           location: str) -> None:
        """
            Проверка поиска и выбора существующей локации.
            :param logged_in_map_page: Фикстура авторизованной MapPage.
            :param location: Название локации для поиска.
        """
        map_page = logged_in_map_page
        map_page.input_location(location)
        map_page.check_location_is_found(location)

    @allure.id("Map-3")
    @allure.feature("Поиск локации")
    @allure.title("Поиск несуществующей локации")
    @allure.description(""" Ввод несуществующей локации в поле поиска""")
    @allure.severity("NORMAL")
    @pytest.mark.parametrize("not_exist_location", ["Самара"])
    @pytest.mark.negative
    def test_location_not_found(self, logged_in_map_page: MapPage,
                                not_exist_location: str) -> None:
        """
            Проверка, что при вводе несуществующей локации выдается сообщение об ошибке.
            :param logged_in_map_page: Фикстура авторизованной MapPage.
            :param not_exist_location: Название локации, которая не должна быть найдена.
        """
        map_page = logged_in_map_page
        map_page.input_location(not_exist_location)
        map_page.check_location_is_not_found(not_exist_location)

    @allure.id("Map-4")
    @allure.feature("Фильтр 'ДТП и АОУ'")
    @allure.title("Открытие меню фильтра 'ДТП и АОУ'")
    @allure.description("""""")
    @allure.severity("CRITICAL")
    @pytest.mark.positive
    def test_open_dtp_aou_menu(self,
                               location_selected_map_page: MapPage) -> None:
        """
            Проверка открытия меню 'ДТП и АОУ' и видимости внутренних фильтров.
            :param location_selected_map_page: Фикстура MapPage с выбранной локацией.
        """
        map_page = location_selected_map_page
        map_page.open_dtp_aou_menu()
        map_page.check_dtp_aou_menu_is_visible()

    @allure.id("Map-5")
    @allure.feature("Фильтр 'ДТП и АОУ'")
    @allure.title("Включение чекбоксов ДТП и АОУ")
    @allure.description("""Включение чекбоксов ДТП и АОУ 
                           и проверка смены атрибута.""")
    @pytest.mark.parametrize("checkbox_name", ALL_MAIN_CHECKBOXES)
    @allure.severity("CRITICAL")
    @pytest.mark.positive
    def test_turn_on_dtp_and_aou(self, location_selected_map_page: MapPage,
                                 checkbox_name: str) -> None:
        """
            Проверка включения основных чекбоксов/переключателей 'ДТП' или 'АОУ'.
            :param location_selected_map_page:
            Фикстура MapPage с выбранной локацией.
            :param checkbox_name: Имя основного чекбокса ('ДТП' или 'АОУ').
        """
        data = ALL_CHECKBOX_DATA[checkbox_name]
        switch_locator = data["main_locator"]
        check_locator = data["check_locator"]
        attribute_name = data["attribute_name"]

        map_page = location_selected_map_page
        map_page.open_dtp_aou_menu()
        map_page.turn_on_checkbox(switch_locator)
        map_page.check_attribute_is_true(check_locator, attribute_name)

    @allure.id("Map-6")
    @allure.feature("Фильтры: ДТП")
    @allure.title("Проверка включения дочернего фильтра ДТП:"
                  " {child_data[name]}")
    @allure.description("""Включение дочерних чекбоксов внутри фильтра ДТП.""")
    @pytest.mark.parametrize("child_data", DTP_CHILDREN_CHECKBOXES)
    @allure.severity("CRITICAL")
    @pytest.mark.positive
    def test_turn_on_checkbox_inside_dtp(
            self,
            location_selected_map_page: MapPage,
            child_data: Dict[str, Union[str, Tuple[str, str]]]) -> None:
        """
            Проверка включения дочернего фильтра ДТП и валидация состояния.
            :param location_selected_map_page:
            Фикстура MapPage с выбранной локацией.
            :param child_data: Словарь с данными дочернего фильтра.
        """
        data = ALL_CHECKBOX_DATA["DTP"]
        switcher_locator = data["main_locator"]
        child_locator = child_data["locator"]
        child_attribute_name = "data-p-checked"

        map_page = location_selected_map_page
        map_page.open_dtp_aou_menu()
        map_page.turn_on_checkbox(switcher_locator)
        map_page.turn_on_checkbox(child_locator)
        map_page.check_attribute_is_true(child_locator, child_attribute_name)

    @allure.id("Map-7")
    @allure.feature("Фильтры: АОУ")
    @allure.title("Проверка переключения радиобаттонов АОУ: "
                  "{child_data[name]}")
    @allure.description("""Включение радиобаттон АОУ""")
    @pytest.mark.parametrize("child_data", AOU_CHILDREN_RADIO)
    @allure.severity("NORMAL")
    @pytest.mark.positive
    def test_turn_on_radio_btn_inside_aou(
            self,
            location_selected_map_page: MapPage,
             child_data: Dict[str, Union[str, Tuple[str, str]]]) -> None:
        """
            Проверка включения дочернего радиобаттона
            АОУ и валидация его состояния.
            :param location_selected_map_page: Фикстура MapPage с выбранной локацией.
            :param child_data: Словарь с данными дочернего фильтра.
        """
        data = ALL_CHECKBOX_DATA["AOU"]
        switcher_locator = data["main_locator"]
        child_locator = child_data["locator"]
        child_check_locator = child_data["check_locator"]
        child_attribute_name = "aria-checked"

        map_page = location_selected_map_page
        map_page.open_dtp_aou_menu()
        map_page.turn_on_checkbox(switcher_locator)
        map_page.turn_on_checkbox(child_locator)
        map_page.check_attribute_is_true(child_check_locator,
                                         child_attribute_name)
