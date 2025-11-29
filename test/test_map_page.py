import allure
import pytest


@allure.parent_suite("Map page")
@allure.suite("Map page")
@allure.description("Work with map page")
class TestMapPage:

    @allure.id("Map-1")
    @allure.feature("Ввод локации в поле поиска")
    @allure.title("Ввод локации")
    @allure.description(""" Ввод локации в поле поиска""")
    @allure.severity("CRITICAL")
    @pytest.mark.parametrize("location", ["Нижний Новгород"])
    @pytest.mark.positive
    def test_positive_location(self, logged_in_map_page, location):
        map_page = logged_in_map_page
        map_page.input_location(location)
        map_page.check_location_is_found(location)

    @allure.id("Map-2")
    @allure.feature("Ввод несуществующей локации в поле поиска")
    @allure.title("Ввод несуществующей локации")
    @allure.description(""" Ввод несуществующей локации в поле поиска""")
    @allure.severity("CRITICAL")
    @pytest.mark.parametrize("not_exist_location", ["Самара"])
    @pytest.mark.negative
    def test_negative_location(self, logged_in_map_page, not_exist_location):
        map_page = logged_in_map_page
        map_page.input_location(not_exist_location)
        map_page.check_location_is_not_found(not_exist_location)

    @allure.id("Map-3")
    @allure.feature("Открытие меню фильтра 'ДТП и АОУ' ")
    @allure.title("")
    @allure.description("""""")
    @allure.severity("CRITICAL")
    @pytest.mark.positive
    def test_open_dtp_aou_menu(self, location_selected_map_page):
        map_page = location_selected_map_page
        map_page.open_dtp_aou_menu()
        map_page.check_dtp_aou_menu_is_visible()
