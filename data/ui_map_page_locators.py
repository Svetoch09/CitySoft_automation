from selenium.webdriver.common.by import By

# Локатор заголовка страницы входа ('Добро пожаловать в СитиСофт')
LOGIN_HEADER = (By.XPATH, "//h1")
# Локатор кнопки выхода на MapPage
LOGOUT_BUTTON = (By.XPATH, "//*[@class='p-menubar-item-icon pi pi-sign-out ng-star-inserted']")

# --- Локаторы поиска локации ---
INPUT_LOCATION_FIELD = (By.XPATH, "//*[@inputid='on_label']")
INPUT_SEARCH_FIELD = (By.XPATH, "//*[@type='search']")
NOT_FOUND_MESSAGE = (By.XPATH, '//*[contains(text(), " Нет доступных вариантов ")]')

# --- Локаторы меню фильтров ДТП и АОУ ---
DTP_AOU_MENU_TITLE = (By.XPATH, "//span[@class='title_text' and text()=' ДТП и АОУ ']")
DTP_FILTER_TITLE = (By.XPATH, "//*[@class='title' and @for='layerДТП']")
AOU_FILTER_TITLE = (By.XPATH, "//*[@class='title' and @for='layerАварийно-опасные участки']")