import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ユーザーとプロジェクトの作成ユーティリティ関数
# def create_user(name="User1", email="user1@example.com"):
#     payload = {
#         "email": email,
#         "password": "testpass123",
#     }
#     response = client.post("/api/user", json=payload)
#     assert response.status_code == 201
#     return response.json()


# def create_project(title="Project1"):
#     payload = {
#         "title": title,
#         "description": "Sample description",
#         "color": "#123456",
#         "image": "",
#         "document": "",
#         "reference": "",
#         "start": "2025-04-03",
#         "deadline": "2025-04-30"
#     }
#     response = client.post("/api/project", json=payload)
#     assert response.status_code == 201
#     return response.json()


# def test_add_user_to_project():
#     user = create_user()
#     project = create_project()

#     res = client.post(
#         f"/api/project/{project['id']}/user",
#         json={"user_id": user["id"], "role": "admin"}
#     )
#     assert res.status_code == 200
#     assert res.json()["message"].lower() == "user added to project"


# def test_get_users_by_project():
#     user = create_user("User2", "user2@example.com")
#     project = create_project("Project2")

#     client.post(
#         f"/api/project/{project['id']}/user",
#         json={"user_id": user["id"], "role": "member"}
#     )

#     res = client.get(f"/api/project/{project['id']}/users")
#     assert res.status_code == 200
#     users = res.json()

#     assert any(u["id"] == user["id"] for u in users)
#     assert any(u["role"] == "member" for u in users)


# def test_get_projects_by_user():
#     user = create_user("User3", "user3@example.com")
#     project = create_project("Project3")

#     client.post(
#         f"/api/project/{project['id']}/user",
#         json={"user_id": user["id"], "role": "editor"}
#     )

#     res = client.get(f"/api/user/{user['id']}/projects")
#     assert res.status_code == 200
#     projects = res.json()

#     assert any(p["id"] == project["id"] for p in projects)
#     assert any(p["role"] == "editor" for p in projects)


# def test_update_user_role_in_project():
#     user = create_user("User4", "user4@example.com")
#     project = create_project("Project4")

#     client.post(
#         f"/api/project/{project['id']}/user",
#         json={"user_id": user["id"], "role": "viewer"}
#     )

#     res = client.put(
#         f"/api/project/{project['id']}/user/{user['id']}",
#         json={"role": "admin"}
#     )
#     assert res.status_code == 200
#     assert res.json()["message"].lower() == "user role updated"

#     res_users = client.get(f"/api/project/{project['id']}/users")
#     target_user = next((u for u in res_users.json() if u["id"] == user["id"]), None)
#     assert target_user is not None
#     assert target_user["role"] == "admin"


# def test_remove_user_from_project():
#     user = create_user("User5", "user5@example.com")
#     project = create_project("Project5")

#     client.post(
#         f"/api/project/{project['id']}/user",
#         json={"user_id": user["id"], "role": "member"}
#     )

#     res = client.delete(f"/api/project/{project['id']}/user/{user['id']}")
#     assert res.status_code == 200
#     assert "deleted" in res.json()["message"].lower()

#     # 削除確認
#     res_users = client.get(f"/api/project/{project['id']}/users").json()
#     assert all(u["id"] != user["id"] for u in res_users)
