from selenium.webdriver.common.by import By

ALL_CHECKBOX_DATA = {
    # свитчер: ДТП
    "DTP": {
        "main_locator": (By.XPATH, "//*[@title='ДТП']//p-toggle-switch[@data-pc-section='root']"),
        "check_locator": (By.XPATH, "//*[@type='checkbox' and @id='layerДТП']"),
        "attribute_name": "aria-checked",
        "expected_value": 'true',
        # Секция дочерних чекбоксов
        "children": [
            {"name": " ДТП без погибших ", "locator": (By.XPATH, "//*[@id='withoutDead']/..")},
            {"name": " ДТП с погибшими ", "locator": (By.XPATH, "//*[@id='withDead']/..")},
            {"name": " ДТП с признаками опьянения ", "locator": (By.XPATH, "//*[@for='alcoholViolation']/../p-checkbox")},
             {"name": " ДТП с неудовлетворительными дорожными условиями ",
              "locator": (By.XPATH, "//*[@id='withNegativeEnvFactors']/..")},
            {"name": " ДТП в местах производства дорожных работ ",
             "locator": (By.XPATH, "//*[@id='inRoadWorkPlaces']/..")}
        ]
    },
    # свитчер: АОУ
    "AOU": {
        "main_locator": (By.XPATH, "//*[@title='Аварийно-опасные участки']"),
        "check_locator": (By.XPATH, "//*[@type='checkbox' and @id='layerАварийно-опасные участки']"),
        "attribute_name": "aria-checked",
        "expected_value": 'true',
        # Секция дочерних радиобаттонов
        "children": [
            {"name": " Сформированные ", "locator": (By.XPATH, "//input[@type='radio' and @id='formed_calculated']/.."),
             "check_locator": (By.XPATH, "//input[@type='radio' and @id='formed_calculated']")},
            {"name": " Потенциальные ", "locator": (By.XPATH, "//input[@type='radio' and @id='preliminary_calculated']/.."),
             "check_locator": (By.XPATH, "//input[@type='radio' and @id='preliminary_calculated']")},
            {"name": " ГАИ ", "locator": (By.XPATH, "//input[@type='radio' and @id='formed_statgibdd']/.."),
             "check_locator": (By.XPATH, "//input[@type='radio' and @id='formed_statgibdd']")}
        ]
    }
}






