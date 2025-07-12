import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.44.1",
    "Platform": "IOS",
    "App-Version": "4.5.0"
}

print("📍 BASE_URL =", BASE_URL)
if not BASE_URL:
    pytest.fail("❌ BASE_URL не установлен! Проверь .env или переменные окружения")


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
        body = response.json().get("result", {})
        token = body.get("token")
        verification_code = body.get("verificationCode") or "1234"  # по умолчанию 1234
        if not token:
            raise ValueError("Token отсутствует в ответе")
        print(f"✅ Получены token и verificationCode: {token}, {verification_code}")
        return {
            "token": token,
            "code": verification_code
        }
    except Exception as e:
        print("⚠️ Ошибка разбора JSON:", e)
        pytest.fail("❌ Не удалось извлечь sms_token или verificationCode из ответа")


@pytest.fixture(scope="session")
def access_token(sms_token):
    payload = {
        "token": sms_token["token"],
        "verificationCode": sms_token["code"]
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
