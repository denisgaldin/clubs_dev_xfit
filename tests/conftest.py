import os
import pytest
import requests
import json
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

BASE_URL = os.getenv("BASE_URL")

print("📍 BASE_URL =", BASE_URL)
if not BASE_URL:
    pytest.fail("❌ BASE_URL не установлен! Проверь .env или переменные окружения")

# Заголовки по умолчанию
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.44.1",
    "Platform": "IOS",
    "App-Version": "4.5.0"
}


@pytest.fixture(scope="session")
def sms_token():
    phone_number = "9000008851"

    print(f"📨 Отправка SMS на номер: {phone_number}")
    payload = {
        "phone": {
            "countryCode": "7",
            "number": phone_number
        }
    }

    response = requests.post(
        f"{BASE_URL}/authorization/sendVerificationCode",
        headers=HEADERS,
        json=payload
    )

    print("➡️ Ответ на отправку кода:", response.status_code, response.text)

    if response.status_code != 200:
        pytest.fail(f"❌ Ошибка при отправке кода: {response.status_code}")

    try:
        token = response.json().get("result", {}).get("token")
        if not token:
            raise ValueError("Token отсутствует в ответе")
        print("✅ SMS Token получен:", token)
        return token
    except Exception as e:
        print("⚠️ Ошибка разбора JSON:", e)
        pytest.fail("❌ Не удалось извлечь SMS токен из ответа")


@pytest.fixture(scope="session")
def access_token(sms_token):
    payload = {
        "token": sms_token,
        "verificationCode": "1234"
    }

    response = requests.post(
        f"{BASE_URL}/authorization/basic",
        headers=HEADERS,
        json=payload
    )

    print("📤 Ответ авторизации:", response.status_code, response.text)

    if response.status_code != 200:
        pytest.fail(f"❌ Ошибка авторизации: {response.status_code}")

    try:
        token = response.json()["result"]["access"]["token"]
        print("✅ Access Token:", token)
        return token
    except Exception as e:
        print("⚠️ Ошибка разбора JSON:", e)
        pytest.fail("❌ Не удалось извлечь access_token из ответа")
