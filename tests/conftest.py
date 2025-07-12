import pytest
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.44.1",
    "Platform": "IOS",
    "App-Version": "4.5.0",
    "Accept": "*/*",
    "Cache-Control": "no-cache"
}


@pytest.fixture(scope="session")
def sms_token():
    phone_number = "9000008851"
    max_attempts = 3

    for attempt in range(max_attempts):
        print(f"📨 Отправка SMS на номер: {phone_number} (попытка {attempt + 1})")

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

        if response.status_code == 200:
            token = response.json()["result"]["token"]
            code = "1234"  # тестовый код
            print(f"✅ Получены token и verificationCode: {token}, {code}")
            return {"token": token, "code": code}

        elif (
                response.status_code == 403 and
                "VERIFICATION_CODE_ALREADY_SEND_PORTAL" in response.text
        ):
            print("⚠️ Код уже отправлен — ждём 60 секунд перед новой попыткой...")
            time.sleep(60)
        else:
            pytest.fail(f"❌ Ошибка при отправке кода: {response.status_code}")

    pytest.fail("❌ Не удалось отправить SMS после нескольких попыток")


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

    print("🔐 Ответ на авторизацию:", response.status_code, response.text)

    if response.status_code != 200:
        pytest.fail(f"❌ Ошибка авторизации: {response.status_code}")

    data = response.json()
    access = data.get("result", {}).get("access", {})
    token = access.get("token")

    if not token:
        pytest.fail("❌ Access token отсутствует в ответе")

    print("✅ Access token получен:", token)
    return token
