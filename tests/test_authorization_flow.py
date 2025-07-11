import os
import pytest
import requests
import json
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

HEADERS_BASIC_AUTH = {
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.44.1",
    "Platform": "IOS",
    "App-Version": "4.5.0",
    "Accept": "*/*",
    "Cache-Control": "no-cache"
}


def test_authorization_by_sms(sms_token):
    payload = {
        "token": sms_token,
        "verificationCode": "1234"
    }

    response = requests.post(
        f"{BASE_URL}/authorization/basic",
        headers=HEADERS_BASIC_AUTH,
        json=payload
    )

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    access = data.get("result", {}).get("access", {})
    assert "token" in access, "❌ Access token отсутствует в ответе"
    print("✅ Access token успешно получен:", access["token"])
