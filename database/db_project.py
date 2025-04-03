from decouple import config
import motor.motor_asyncio
from typing import Optional, Union
from bson import ObjectId
from fastapi import HTTPException 

from auth_utils import AuthJwtCsrf
from .db_task import task_serializer


MONGO_API_KEY = config("MONGO_API_KEY")


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
database = client.API_DB
collection_project = database.project
collection_task = database.task

auth = AuthJwtCsrf()

def project_serializer(project: dict) -> dict:
    """MongoDB のプロジェクトデータをシリアライズ"""
    return {
        "id": str(project["_id"]),
        "title": project.get("title", ""),
        "description": project.get("description", ""),
        "color": project.get("color", "#FFFFFF"),
        "image": project.get("image", ""),
        "document": project.get("document", ""),
        "reference": project.get("reference", ""),
        "start": project.get("start", "") if project.get("start") else "",
        "deadline": project.get("deadline", "") if project.get("deadline") else "",
    }




async def db_create_project(data :dict) ->Union[dict, bool]:
    project = await collection_project.insert_one(data)
    new_project = await collection_project.find_one({"_id": project.inserted_id})
    if new_project:
        return project_serializer(new_project)
    return False

async def db_get_projects() -> list:
    projects = []
    async for project in collection_project.find():
        projects.append(project_serializer(project))
    return projects

async def db_get_single_project(id: str) -> Union[dict, bool]:
    project = await collection_project.find_one({"_id": ObjectId(id)})
    if project:
        return project_serializer(project)
    return False


async def db_update_project(id: str, data: dict) -> Union[dict, bool]:
    project = await collection_project.find_one({"_id": ObjectId(id)})
    if project:
        await collection_project.update_one({"_id": ObjectId(id)}, {"$set": data})
        updated_project = await collection_project.find_one({"_id": ObjectId(id)})
        if updated_project.modified_count > 0:
            return project_serializer(updated_project)
    return False

async def db_delete_project(id: str) -> bool:
    project = await collection_project.find_one({"_id": ObjectId(id)})
    if project:
        await collection_project.delete_one({"_id": ObjectId(id)})
        return True
    return False


async def db_get_tasks_by_project(project_id: str) -> list:
    """特定の project_id に紐づいたタスク一覧を取得"""
    tasks = []
    async for task in collection_task.find({"project_id": project_id}):
        tasks.append(task_serializer(task))
    return tasks

async def db_get_tasks_by_user(user_id: str) -> list:
    """特定の user_id に紐づいたタスク一覧を取得"""
    tasks = []
    async for task in collection_task.find({"user_id": user_id}):
        tasks.append(task_serializer(task))
    return tasks

