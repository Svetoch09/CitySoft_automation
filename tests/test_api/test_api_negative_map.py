import allure
import pytest

from data.api_dtp_data import DTP_NEGATIVE_SCENARIOS

@allure.parent_suite("API tests")
@allure.suite("API Map page")
@allure.description("Тестирование негативных сценариев и валидации данных DTP.")
@pytest.mark.api
@pytest.mark.negative # <-- Метка для негативных тестов
class TestApiMapPageNegative:
    @allure.id("API-Map-N-1")
    @allure.feature("Валидация фильтров DTP")
    @allure.title("Валидация невалидных данных фильтрации: {scenario_description}")
    @allure.description("Проверка, что сервер возвращает 400 при некорректном формате или значении.")
    @allure.severity("BLOCKER")
    @pytest.mark.parametrize("filter_key, filter_value, scenario_description",
        DTP_NEGATIVE_SCENARIOS)
    def test_dtp_wrong_data_scenarios(self, map_service, dtp_base_body, filter_key,
                                  filter_value, scenario_description):
        """
            Набор параметризованных тестов на валидацию входных данных
            (Data Validation) для API-эндпоинта фильтрации ДТП
        """
        allure.dynamic.title(f"Валидация: {scenario_description}")

        dtp_base_body[filter_key] = filter_value
        url_end = "/all/by_filters"

        response = map_service.search_dtp_data_by_filters(url_end, dtp_base_body)
        map_service.check_status_code(response, 400)
        map_service.check_content_type_json(response)

    @allure.id("API-Map-N-2")
    @allure.feature("Чтение данных по ID")
    @allure.title("Обработка запроса несуществующего ID: {dtp_id}")
    @allure.description("Проверка корректной обработки запроса на несуществующую карточку ДТП.")
    @allure.severity("BLOCKER")
    @pytest.mark.parametrize("dtp_id", ["22100123500"])
    def test_get_dtp_info_by_wrong_id(self, map_service, dtp_id):
        """ Корректнная обработка запроса несуществующей карточки ДТП"""

        allure.dynamic.title(f"Обработка несуществующего ID: {dtp_id}")

        url_end = "/all/extended_info/"
        expected_data = f"Dtp card id={dtp_id} not found."

        response = map_service.get_dtp_by_id(url_end, dtp_id)

        map_service.check_status_code(response)
        map_service.check_content_type_json(response)
        dtp_data = map_service.get_and_validate_json_body(response)

        expected_fields = ["hostname", "data"]
        map_service.check_mandatory_fields(dtp_data, expected_fields)
        map_service.check_field_type(dtp_data, "data", str)
        map_service.check_data_in_response(dtp_data, expected_data)