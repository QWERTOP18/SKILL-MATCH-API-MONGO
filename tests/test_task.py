# tests/test_task.py
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_create_task():
    response = client.post(
        "/api/task",
        json={"title": "Test Task", "description": "This is a test task"}
    )
    assert response.status_code == 200
    assert response.json() == {"title": "Test Task", "description": "This is a test task"}

def test_get_tasks():
    # 最初にタスクを作成
    client.post(
        "/api/task",
        json={"title": "Test Task", "description": "This is a test task"}
    )

    # タスク一覧を取得
    response = client.get("/api/task")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test Task"
