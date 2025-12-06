DTP_FILTER_BASE_BODY = {
    "areaFilterParams": {
        "bbox": {
            "minLon": 48.8205846000001,
            "minLat": 55.603478,
            "maxLon": 49.3812468999993,
            "maxLat": 55.9382194,
        },
        "regionIds": [],
        "districtIds": [],
        "localityIds": [113664],
        "cityDistrictIds": [],
        "roadIds": [],
    },
    "zonedDateFilterParams": {
        "dateFrom": "2019-12-31T23:00:00.000Z",
        "dateTo": "2020-01-01T22:59:59.999Z",
    },
    "withDeadOrNot": "ALL_DTP",
    "withNegativeEnvFactors": False,
    "inRoadWorkPlaces": False,
    "alcoholViolation": False,
    "onlyInEmergencyAreas": False,
    "dtpDescriptionIds": [],
}

DTP_FILTER_SCENARIOS = [
    # (Имя_фильтра, Ожидаемый_результат, Описание)
    ("BASE_SCENARIO", None, "Базовая проверка фильтра без активных условий"),
    ("withDeadOrNot", "WITHOUT_DEAD", "ДТП без погибших"),
    ("withNegativeEnvFactors", True,
     "ДТП с неудовлетворительными дорожными условиями"),
    ("inRoadWorkPlaces", True, "ДТП в местах производства дорожных работ"),
    ("alcoholViolation", True, "ДТП с признаками опьянения"),
    ("onlyInEmergencyAreas", True, "ДТП только в опасных зонах"),
]

DTP_NEGATIVE_SCENARIOS = [
    ("areaFilterParams", "Kazan", "Неверные данные"),
    ("zonedDateFilterParams",
        {"dateFrom": "2019-12-31T23:00:00", "dateTo": "2020-12-31T22:59:59"},
        "Неверный формат веремени"),
    ("withDeadOrNot", "Yes", "Неверные данные"),
    ("withDeadOrNot", 123, "Неверный формат данных"),
]
