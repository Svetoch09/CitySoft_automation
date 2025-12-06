import pytest
import allure

from data.api_dtp_data import DTP_FILTER_SCENARIOS
from src.api.DTPService import DTPService
from src.api.UserService import UserService
from typing import Dict, Any


@allure.parent_suite("API tests")
@allure.suite("API Map page")
@allure.description("Тестирование основных эндпоинтов DTP и UserInfo.")
@pytest.mark.api
@pytest.mark.positive
class TestApiMapPage:

    @allure.id("API-USER_INFO-1")
    @allure.feature("Авторизация")
    @allure.title("Успешное получение UserInfo")
    @allure.description("Проверка статуса 200 и базовой схемы UserInfo.")
    @allure.severity("NORMAL")
    def test_get_userinfo_success(self, user_service: UserService) -> None:
        """
            Тест: успешное получение информации о
            пользователе с валидной авторизацией.
            :param user_service: Фикстура сервиса UserService.
        """
        response = user_service.get_user_info()

        user_service.check_status_code(response)
        user_service.check_content_type_json(response)
        user_info_data = user_service.get_and_validate_json_body(response)

        expected_fields = ["sub", "email_verified", "name"]
        user_service.check_mandatory_fields(user_info_data, expected_fields)
        user_service.check_field_type(user_info_data, "name", str)

    @allure.id("API-Map-1")
    @allure.feature("Фильтрация данных ДТП")
    @allure.title("Проверка различных сценариев фильтрации")
    @allure.description(
        "Проверка активации булевых фильтров ДТП, проверка статуса 200 "
    )
    @allure.severity("CRITICAL")
    @pytest.mark.parametrize(
        "filter_key, filter_value, scenario_description", DTP_FILTER_SCENARIOS
    )
    def test_dtp_filter_scenarios(
            self,
            map_service: DTPService,
            dtp_base_body: Dict[str, Any],
            filter_key: str,
            filter_value: Any,
            scenario_description: str) -> None:
        """
            Тест проверяет базовую структуру, а затем различные фильтры DTP.
            :param map_service: Фикстура сервиса DTPService.
            :param dtp_base_body: Тело запроса, содержащее базовые фильтры.
            :param filter_key: Имя поля, которое нужно изменить.
            :param filter_value: Новое булево значение.
        """
        allure.dynamic.title(f"Проверка фильтра: {scenario_description}")
        if filter_key != "BASE_SCENARIO":
            dtp_base_body[filter_key] = filter_value

        url_end = "/all/by_filters"

        response = map_service.search_dtp_data_by_filters(
            url_end, dtp_base_body)

        map_service.check_status_code(response)
        map_service.check_content_type_json(response)
        dtp_data = map_service.get_and_validate_json_body(response)

        expected_fields = ["hostname", "data"]
        map_service.check_mandatory_fields(dtp_data, expected_fields)
        map_service.check_field_type(dtp_data, "data", dict)

    @allure.id("API-Map-2")
    @allure.feature("Чтение данных по ID")
    @allure.title("Получение расширенной информации о ДТП по ID")
    @allure.description(
        "Проверка успешного получения детальной карточки "
        "ДТП и валидация возвращенного ID.Проверка статуса 200 "
    )
    @allure.severity("CRITICAL")
    @pytest.mark.parametrize("dtp_id", ["221001235"])
    def test_get_dtp_info_by_id(self, map_service: DTPService,
                                dtp_id: str) -> None:
        """
            Успешное получение информации о ДТП по id.
            :param map_service: Фикстура сервиса DTPService.
            :param dtp_id: Параметризованный ID карточки ДТП.
        """
        allure.dynamic.title(f"Получение расширенной"
                             f" информации о ДТП по ID: {dtp_id}")

        url_end = "/all/extended_info/"
        response = map_service.get_dtp_by_id(url_end, dtp_id)

        map_service.check_status_code(response)
        map_service.check_content_type_json(response)
        dtp_data = map_service.get_and_validate_json_body(response)

        expected_fields = ["hostname", "data"]
        map_service.check_mandatory_fields(dtp_data, expected_fields)
        map_service.check_field_type(dtp_data, "data", dict)
        map_service.check_dtp_id_in_data(dtp_data, dtp_id)
