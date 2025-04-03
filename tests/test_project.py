# tests/test_project.py
import pytest
from fastapi.testclient import TestClient
from main import app



client = TestClient(app)

def test_create_project():
    project_data = {
        "title": "New Project",
        "description": "Project description",
        "color": "#FF5733",
        "image": "",
        "document": "document_url",
        "reference": "reference_url",
        "start": "2025-04-03",
        "deadline": "2025-04-03"
    }

    response = client.post("/api/project", json=project_data)

    # ステータスコードが201 Createdであることを確認
    assert response.status_code == 201

    # レスポンスデータから 'id' を削除して比較
    response_json = response.json()
    response_json.pop("id", None) 

    #
    assert response_json == project_data

   

def test_get_projects():
    # プロジェクト追加前のカウントを取得
    response_before = client.get("/api/project")
    assert response_before.status_code == 200
    count_before = len(response_before.json())

    # 新しいプロジェクトを作成
    client.post(
        "/api/project",
        json={
            "title": "Test Project",
            "description": "string",
            "color": "#FFFFFF",
            "image": "image_url",
            "document": "document_url",
            "reference": "reference_url",
            "start": "2025-04-03",
            "deadline": "2025-04-03"
        }
    )

    # プロジェクト追加後のカウントを取得
    response_after = client.get("/api/project")
    assert response_after.status_code == 200
    count_after = len(response_after.json())

    # プロジェクトが1つ増えていることを確認
    assert count_after == count_before + 1
    assert response_after.json()[-1]["title"] == "Test Project"  # 最後のプロジェクトが期待通りか確認


def test_update_project():
    # 最初にプロジェクトを作成
    response = client.post(
        "/api/project",
        json={
            "title": "Original Project",
            "description": "string",
            "color": "#FFFFFF",
            "image": "image_url",
            "document": "document_url",
            "reference": "reference_url",
            "start": "2025-04-03",
            "deadline": "2025-04-03"
        }
    )

    # プロジェクトが作成された後、IDを取得
    project_id = response.json()["id"]

    # 更新するデータ
    updated_data = {
        "title": "Updated Project",
        "description": "Updated description",
        "color": "#000000",
        "image": "new_image_url",
        "document": "new_document_url",
        "reference": "new_reference_url",
        "start": "2025-05-03",
        "deadline": "2025-05-03"
    }

    # PUTリクエストでプロジェクトを更新
    response = client.put(f"/api/project/{project_id}", json=updated_data)
    
    # ステータスコードが200 OKであることを確認
    assert response.status_code == 200

    # レスポンスが更新されたプロジェクトの内容と一致することを確認
    response_json = response.json()
    response_json.pop("id", None)  # idを除去して比較

    assert response_json == updated_data

    # データベースに反映されたか再確認
    # response = client.get(f"/api/project/{project_id}")
    # assert response.status_code == 200
    # assert response.json()["title"] == "Updated Project"
    # assert response.json()["description"] == "Updated description"
    # assert response.json()["color"] == "#000000"
    # assert response.json()["image"] == "new_image_url"
    # assert response.json()["document"] == "new_document_url"
    # assert response.json()["reference"] == "new_reference_url"
