from decouple import config
import motor.motor_asyncio
from typing import Optional, Union
from bson import ObjectId
from fastapi import HTTPException 

from auth_utils import AuthJwtCsrf


MONGO_API_KEY = config("MONGO_API_KEY")


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
database = client.API_DB
collection_task = database.task

auth = AuthJwtCsrf()


def task_serializer(task) -> dict:
    if isinstance(task, dict):
        return task  # task がすでに辞書型であればそのまま返す
    return task.dict()  # Pydantic モデルのインスタンスであれば、dict() を使って辞書に変換
    


async def db_create_task(data :dict) ->Union[dict, bool]:
    task = await collection_task.insert_one(data)
    new_task = await collection_task.find_one({"_id": task.inserted_id})
    if new_task:
        return task_serializer(new_task)
    return False

async def db_get_tasks() -> list:
    tasks = []
    async for task in collection_task.find():
        tasks.append(task_serializer(task))
    return tasks

async def db_get_single_task(id: str) -> Union[dict, bool]:
    task = await collection_task.find_one({"_id": ObjectId(id)})
    if task:
        return task_serializer(task)
    return False


async def db_update_task(id: str, data: dict) -> Union[dict, bool]:
    task = await collection_task.find_one({"_id": ObjectId(id)})
    if task:
        await collection_task.update_one({"_id": ObjectId(id)}, {"$set": data})
        updated_task = await collection_task.find_one({"_id": ObjectId(id)})
        if updated_task.modified_count > 0:
            return task_serializer(updated_task)
    return False

async def db_delete_task(id: str) -> bool:
    task = await collection_task.find_one({"_id": ObjectId(id)})
    if task:
        await collection_task.delete_one({"_id": ObjectId(id)})
        return True
    return False
