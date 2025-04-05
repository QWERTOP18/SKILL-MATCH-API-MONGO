from decouple import config
import motor.motor_asyncio
from typing import Optional, Union
from bson import ObjectId
from fastapi import HTTPException 
from datetime import datetime, timedelta
import asyncio
from app.auth_utils import AuthJwtCsrf

MONGO_API_KEY = config("MONGO_API_KEY")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
client.get_io_loop = asyncio.get_event_loop

database = client.API_DB
collection_task = database.task

auth = AuthJwtCsrf()

def task_serializer(task: dict) -> dict:
    """MongoDB のタスクデータをシリアライズ"""
    return {
        "id": str(task["_id"]),
        "user_id": task.get("user_id", ""),
        "project_id": task.get("project_id", ""),
        "title": task.get("title", ""),
        "description": task.get("description", ""),
        "color": task.get("color", "#FFFFFF"),
        "status": task.get("status", ""),
        "technical_skill": task.get("technical_skill", 0),
        "problem_solving_ability": task.get("problem_solving_ability", 0),
        "communication_skill": task.get("communication_skill", 0),
        "security_awareness": task.get("security_awareness", 0),
        "leadership_and_collaboration": task.get("leadership_and_collaboration", 0),
        "frontend_skill": task.get("frontend_skill", 0),
        "backend_skill": task.get("backend_skill", 0),
        "infrastructure_skill": task.get("infrastructure_skill", 0),
    }

async def db_create_task(data: dict) -> Union[dict, bool]:
    """新しいタスクをデータベースに作成"""
    task = await collection_task.insert_one(data)
    new_task = await collection_task.find_one({"_id": task.inserted_id})
    return task_serializer(new_task) if new_task else False

async def db_get_tasks() -> list:
    """全タスクを取得"""
    tasks = []
    async for task in collection_task.find():
        tasks.append(task_serializer(task))
    return tasks

async def db_get_single_task(id: str) -> Union[dict, bool]:
    """指定したIDのタスクを取得"""
    task = await collection_task.find_one({"_id": ObjectId(id)})
    return task_serializer(task) if task else False

async def db_update_task(id: str, data: dict) -> Union[dict, bool]:
    task = await collection_task.find_one({"_id": ObjectId(id)})
    if task:
        # dataが辞書でなければ、dictに変換
        update_data = data if isinstance(data, dict) else data.model_dump()
        result = await collection_task.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        if result.modified_count > 0:
            updated_task = await collection_task.find_one({"_id": ObjectId(id)})
            return task_serializer(updated_task)
    return False

async def db_delete_task(id: str) -> bool:
    """タスクを削除"""
    result = await collection_task.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
