from decouple import config
import motor.motor_asyncio
from typing import Optional, Union
from bson import ObjectId


MONGO_API_KEY = config("MONGO_API_KEY")


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
database = client.API_DB
collection_todo = database.todo
collection_user = database.user


def todo_serializer(todo) ->dict:
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo["description"]
    }



async def db_create_todo(data :dict) ->Union[dict, bool]:
    todo = await collection_todo.insert_one(data)
    # todoにはinserted_idが入っている
    new_todo = await collection_todo.find_one({"_id": todo.inserted_id})
    if new_todo:
        return todo_serializer(new_todo)
    return False

async def db_get_todos() -> list:
    todos = []
    async for todo in collection_todo.find():
        todos.append(todo_serializer(todo))
    return todos

async def db_get_single_todo(id: str) -> Union[dict, bool]:
    todo = await collection_todo.find_one({"_id": ObjectId(id)})
    if todo:
        return todo_serializer(todo)
    return False


async def db_update_todo(id: str, data: dict) -> Union[dict, bool]:
    todo = await collection_todo.find_one({"_id": ObjectId(id)})
    if todo:
        await collection_todo.update_one({"_id": ObjectId(id)}, {"$set": data})
        updated_todo = await collection_todo.find_one({"_id": ObjectId(id)})
        if updated_todo.modified_count > 0:
            return todo_serializer(updated_todo)
    return False

async def db_delete_todo(id: str) -> bool:
    todo = await collection_todo.find_one({"_id": ObjectId(id)})
    if todo:
        await collection_todo.delete_one({"_id": ObjectId(id)})
        return True
    return False