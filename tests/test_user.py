# tests/test_user.py
import pytest
from fastapi.testclient import TestClient
from main import app



client = TestClient(app)

def test_create_user():
    response = client.post(
        "/api/user",
        json={"username": "test_user", "email": "test@example.com"}
    )
    assert response.status_code == 200
    assert response.json() == {"username": "test_user", "email": "test@example.com"}

def test_get_users():
    # 最初にユーザーを作成
    client.post(
        "/api/user",
        json={"username": "test_user", "email": "test@example.com"}
    )

    # ユーザー一覧を取得
    response = client.get("/api/user")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["username"] == "test_user"
