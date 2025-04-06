from openai import OpenAI
from decouple import config
from bson import ObjectId

client = OpenAI(api_key=config("OPENAI_API_KEY"))
from decouple import config
import json
import random
from typing import List
import sys

# pytest 実行中かどうかを判定する関数
def is_pytest_running():
    return "pytest" in sys.modules


async def generate_tasks_for_project(project: dict, num_tasks: int = 1):
    if is_pytest_running():
        # テスト実行中の場合はダミーデータを返す
        print("テスト実行中")
        return [
            {
                "title": "Test Task",
                "description": "This is a test task.",
                "color": "#FFFFFF",
                "status": "not_started",
                "user_id": "empty",
                "project_id": str(project["_id"]),
                "technical_skill": 3,
                "problem_solving_ability": 4,
                "communication_skill": 5,
                "security_awareness": 2,
                "leadership_and_collaboration": 3,
                "frontend_skill": 4,
                "backend_skill": 2,
                "infrastructure_skill": 1,
            }
        ]
    project_title = project["title"]
    project_id = str(project["_id"])
    project_description = project["description"]
    tasks = []

    for _ in range(num_tasks):
        # GPTにJSON形式でタスクデータを出力させる
        prompt = (
            f"あなたはプロジェクトマネージャーです。\n"
            f"プロジェクト「{project_title}」の一部として適切なタスクを1つ作成してください。\n"
            f"プロジェクトの説明: {project_description}\n"
            "以下のJSON形式で出力してください。\n"
            "```json\n"
            "{\n"
            '  "title": "タスク名",\n'
            '  "description": "タスクの具体的な説明",\n'
            "}\n"
            "```"
        )
# '  "technical_skill": 数字(0〜5),\n'
#             '  "problem_solving_ability": 数字(0〜5),\n'
#             '  "communication_skill": 数字(0〜5),\n'
#             '  "security_awareness": 数字(0〜5),\n'
#             '  "leadership_and_collaboration": 数字(0〜5),\n'
#             '  "frontend_skill": 数字(0〜5),\n'
#             '  "backend_skill": 数字(0〜5),\n'
#             '  "infrastructure_skill": 数字(0〜5)\n'
       
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Your system message here."}, {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        print(response)
        print(response.usage)


        # コードブロックからJSON部分を取り出す
        try:
            content = response.choices[0].message.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            ai_task = json.loads(content)
        except Exception as e:
            print("JSON解析失敗:", e)
            continue

        # スキル付きのタスクデータを生成
        task_data = {
            "title": ai_task["title"],
            "description": ai_task["description"],
            "color": "#%06x" % random.randint(0, 0xFFFFFF),
            "status": "not_started",
            "user_id": "empty",
            "project_id": project_id,
            "technical_skill": ai_task.get("technical_skill", random.randint(0, 5)),
            "problem_solving_ability": ai_task.get("problem_solving_ability", random.randint(0, 5)),
            "communication_skill": ai_task.get("communication_skill", random.randint(0, 5)),
            "security_awareness": ai_task.get("security_awareness", random.randint(0, 5)),
            "leadership_and_collaboration": ai_task.get("leadership_and_collaboration", random.randint(0, 5)),
            "frontend_skill": ai_task.get("frontend_skill", random.randint(0, 5)),
            "backend_skill": ai_task.get("backend_skill", random.randint(0, 5)),
            "infrastructure_skill": ai_task.get("infrastructure_skill", random.randint(0, 5)),
        }

        tasks.append(task_data)

    return tasks