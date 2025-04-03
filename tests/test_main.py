import pytest
from httpx import AsyncClient
from main import app  # FastAPI アプリをインポート

@pytest.mark.asyncio
async def test_create_todo():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/todo", json={
            "title": "Test Todo",
            "description": "This is a test",
            "done": False
        })
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["title"] == "Test Todo"
        assert data["description"] == "This is a test"
        assert data["done"] is False

@pytest.mark.asyncio
async def test_get_todos():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/todo")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_single_todo():
    # まずタスクを作成
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_response = await client.post("/api/todo", json={
            "title": "Single Task",
            "description": "Test getting a single task",
            "done": False
        })
        created_data = create_response.json()
        task_id = created_data["id"]

        # 作成したタスクを取得
        response = await client.get(f"/api/todo/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Single Task"

@pytest.mark.asyncio
async def test_update_todo():
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_response = await client.post("/api/todo", json={
            "title": "Old Task",
            "description": "Old description",
            "done": False
        })
        task_id = create_response.json()["id"]

        # 更新リクエスト
        response = await client.put(f"/api/todo/{task_id}", json={
            "title": "Updated Task",
            "description": "Updated description",
            "done": True
        })
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Task"
        assert data["description"] == "Updated description"
        assert data["done"] is True

@pytest.mark.asyncio
async def test_delete_todo():
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_response = await client.post("/api/todo", json={
            "title": "Task to delete",
            "description": "This will be deleted",
            "done": False
        })
        task_id = create_response.json()["id"]

        # タスクを削除
        response = await client.delete(f"/api/todo/{task_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Task deleted successfully"}

        # 削除されたタスクを取得しようとするとエラーになるはず
        response = await client.get(f"/api/todo/{task_id}")
        assert response.status_code == 404
