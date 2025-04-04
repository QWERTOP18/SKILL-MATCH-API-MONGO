import csv
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_questions():
    # CSV ファイルの内容を読み込む
    with open("app/seed/questions.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        expected = list(reader)

    response = client.get("/questions")
    assert response.status_code == 200

    actual = response.json()

    # 内容が一致するかチェック
    assert actual == expected
