# tests/test_project.py
import pytest
from fastapi.testclient import TestClient
from app.main import app



client = TestClient(app)

def test_create_project():
    response = client.post(
        "/api/project",
        json={"name": "Test Project", "description": "This is a test project"}
    )
    assert response.status_code == 200
    assert response.json() == {"name": "Test Project", "description": "This is a test project"}

def test_get_projects():
    # 最初にプロジェクトを作成
    client.post(
        "/api/project",
        json={"name": "Test Project", "description": "This is a test project"}
    )

    # プロジェクト一覧を取得
    response = client.get("/api/project")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Test Project"
