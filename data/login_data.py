import os

# --- 1. Извлечение данных из .env ---

VALID_LOGIN = os.getenv("TEST_LOGIN")
VALID_PASSWORD = os.getenv("TEST_PASSWORD")
INVALID_LOGIN = os.getenv("INVALID_LOGIN")
INVALID_PASSWORD = os.getenv("INVALID_PASSWORD")

# --- 2. Массив негативных кейсов ---
NEGATIVE_LOGIN_CASES = [
    # 1. Неверные оба
    (INVALID_LOGIN, INVALID_PASSWORD, "Ошибка в логине или пароле"),
    # 2. Верный логин, неверный пароль
    (VALID_LOGIN, INVALID_PASSWORD, "Ошибка в логине или пароле"),
    # 3. Неверный логин, верный пароль
    (INVALID_LOGIN, VALID_PASSWORD, "Ошибка в логине или пароле"),
    # 4. Пустой логин
    ("", VALID_PASSWORD, "Ошибка в логине или пароле"),
    # 5. Пустой пароль
    (VALID_LOGIN, "", "Ошибка в логине или пароле"),
]