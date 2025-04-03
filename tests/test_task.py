# tests/test_task.py
import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_get_task_not_found():
    # 存在しないタスクIDでAPIエンドポイントをテスト
    response = client.get("/api/task/507f1f77bcf86cd799439000")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_create_task():
    response = client.post(
        "/api/task",
        json={
            "technical_skill": 0,
            "problem_solving_ability": 0,
            "communication_skill": 0,
            "security_awareness": 0,
            "leadership_and_collaboration": 0,
            "frontend_skill": 0,
            "backend_skill": 0,
            "infrastructure_skill": 0,
            "title": "string",
            "description": "string",
            "color": "#FFFFFF",
            "status": "string",
            "user_id": "string",
            "project_id": "string"
        }
    )
    assert response.status_code == 201
    
    # レスポンス JSON を取得し、`id` を削除してtest
    response_json = response.json()
    response_json.pop("id", None)

    expected_json = {
        "technical_skill": 0,
        "problem_solving_ability": 0,
        "communication_skill": 0,
        "security_awareness": 0,
        "leadership_and_collaboration": 0,
        "frontend_skill": 0,
        "backend_skill": 0,
        "infrastructure_skill": 0,
        "title": "string",
        "description": "string",
        "color": "#FFFFFF",
        "status": "string",
        "user_id": "string",
        "project_id": "string"
    }

    assert response_json == expected_json

def test_get_tasks():
    # タスク追加前のカウントを取得
    response_before = client.get("/api/task")
    assert response_before.status_code == 200
    count_before = len(response_before.json())

    # 新しいタスクを作成
    client.post(
        "/api/task",
        json={
            "technical_skill": 0,
            "problem_solving_ability": 0,
            "communication_skill": 0,
            "security_awareness": 0,
            "leadership_and_collaboration": 0,
            "frontend_skill": 0,
            "backend_skill": 0,
            "infrastructure_skill": 0,
            "title": "Test Task",
            "description": "string",
            "color": "#FFFFFF",
            "status": "string",
            "user_id": "string",
            "project_id": "string"
        }
    )

    # タスク追加後のカウントを取得
    response_after = client.get("/api/task")
    assert response_after.status_code == 200
    count_after = len(response_after.json())

    # タスクが1つ増えていることを確認
    assert count_after == count_before + 1
    assert response_after.json()[-1]["title"] == "Test Task"  # 最後のタスクが期待通りか確認

def test_update_task():
    # 最初にタスクを作成
    response = client.post(
        "/api/task",
        json={
            "technical_skill": 0,
            "problem_solving_ability": 0,
            "communication_skill": 0,
            "security_awareness": 0,
            "leadership_and_collaboration": 0,
            "frontend_skill": 0,
            "backend_skill": 0,
            "infrastructure_skill": 0,
            "title": "Original Task",
            "description": "string",
            "color": "#FFFFFF",
            "status": "string",
            "user_id": "string",
            "project_id": "string"
        }
    )

    # タスクが作成された後、IDを取得
    task_id = response.json()["id"]

    # 更新するデータ
    updated_data = {
        "technical_skill": 5,
        "problem_solving_ability": 5,
        "communication_skill": 5,
        "security_awareness": 5,
        "leadership_and_collaboration": 5,
        "frontend_skill": 5,
        "backend_skill": 5,
        "infrastructure_skill": 5,
        "title": "Updated Task",
        "description": "Updated description",
        "color": "#000000",
        "status": "In Progress",
        "user_id": "string",
        "project_id": "string"
    }

    # PUTリクエストでタスクを更新
    response = client.put(f"/api/task/{task_id}", json=updated_data)
    
    # ステータスコードが200 OKであることを確認
    assert response.status_code == 200

    # レスポンスが更新されたタスクの内容と一致することを確認
    response_json = response.json()
    response_json.pop("id", None)  # idを除去して比較

    assert response_json == updated_data

    # データベースに反映されたか再確認
    # response = client.get(f"/api/task/{task_id}")
    # assert response.status_code == 200
    # assert response.json()["title"] == "Updated Task"
    # assert response.json()["description"] == "Updated description"
    # assert response.json()["color"] == "#000000"
    # assert response.json()["status"] == "In Progress"


