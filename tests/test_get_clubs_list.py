import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

HEADERS_CLUBS_LIST = {
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.44.1",
    "Accept": "*/*",
    "Cache-Control": "no-cache",
}


def test_get_clubs_list(access_token):
    headers = HEADERS_CLUBS_LIST.copy()
    headers["token"] = access_token  # Используем ключ "token" в нижнем регистре

    params = {
        "lat": "55.754202886759",
        "lon": "37.715222611779"
    }

    response = requests.get(
        f"{BASE_URL}/clubs/list",
        headers=headers,
        params=params
    )

    print("📥 Ответ сервера:", response.status_code)
    print("📄 Тело ответа:", response.text)

    assert response.status_code == 200, f"❌ Expected 200, got {response.status_code}\n{response.text}"

    data = response.json()
    assert "result" in data, "❌ В ответе нет поля 'result'"
    print(f"✅ Получено {len(data['result'])} клубов")
