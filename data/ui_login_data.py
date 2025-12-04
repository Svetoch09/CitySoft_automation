import os

# --- 1. Извлечение данных из .env ---
VALID_LOGIN = os.getenv("TEST_LOGIN")
VALID_PASSWORD = os.getenv("TEST_PASSWORD")
INVALID_LOGIN = os.getenv("INVALID_LOGIN")
INVALID_PASSWORD = os.getenv("INVALID_PASSWORD")

# --- 2. Массив негативных кейсов ---
NEGATIVE_LOGIN_CASES = [
    (INVALID_LOGIN, INVALID_PASSWORD, "Ошибка в логине или пароле"),
    (VALID_LOGIN, INVALID_PASSWORD, "Ошибка в логине или пароле"),
    (INVALID_LOGIN, VALID_PASSWORD, "Ошибка в логине или пароле"),
    ("", VALID_PASSWORD, "Ошибка в логине или пароле"),
    (VALID_LOGIN, "", "Ошибка в логине или пароле"),
    ("", "", "Ошибка в логине или пароле"),
]
