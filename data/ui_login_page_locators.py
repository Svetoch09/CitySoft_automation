from selenium.webdriver.common.by import By

# --- Локаторы формы входа ---
INPUT_USERNAME_FIELD = (By.ID, "username")
INPUT_PASSWORD_FIELD = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "kc-login")
ERROR_MESSAGE_CONTAINER = (By.ID, "input-error")

# --- Дополнительные локаторы (для проверок) ---
# заголовок 'Добро пожаловать в СитиСофт'
LOGIN_PAGE_HEADER = (By.XPATH, "//h1")