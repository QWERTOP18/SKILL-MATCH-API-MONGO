from bson import ObjectId
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
import asyncio

# MongoDB接続設定
MONGO_API_KEY = config("MONGO_API_KEY")
client = AsyncIOMotorClient(MONGO_API_KEY)
client.get_io_loop = asyncio.get_event_loop
database = client.API_DB
collection_message = database.message
collection_user = database.user

def serialize_message(message: dict) -> dict:
    """MongoDBのメッセージをAPIレスポンス用に整形"""
    return {
        "_id": str(message["_id"]),
        "user_id": message["user_id"],
        "project_id": message["project_id"],
        "context": message["context"],
        "data": message["data"],
    }

async def serialize_messages_with_user_name(message: dict) -> dict:
   
        user = await collection_user.find_one({"_id": ObjectId(message["user_id"])})
        user_name = user["name"] if user and "name" in user else "NoName"

        return({
            "_id": str(message["_id"]),
            "user_id": message["user_id"],
            "user_name": user_name,
            "project_id": message["project_id"],
            "context": message["context"],
            "data": message["data"],
        })

async def get_serialized_messages(messages: list[dict]) -> list[dict]:
    # 非同期関数を並列実行
    tasks = [serialize_messages_with_user_name(m) for m in messages]
    return await asyncio.gather(*tasks)

# メッセージのCRUD操作
async def create_message(user_id: str, project_id: str, context: str, data: datetime) -> dict:
    message = {
        "user_id": user_id,
        "project_id": project_id,
        "context": context,
        "data": data
    }
    result = await collection_message.insert_one(message)
    return {"message_id": str(result.inserted_id)}

async def get_messages_by_project(project_id: str, skip: int = 0, limit: int = 10) -> List[dict]:
    # プロジェクトIDに基づいてメッセージを検索
    messages = await collection_message.find({"project_id": project_id}).skip(skip).limit(limit).to_list(length=limit)
    tasks = [serialize_messages_with_user_name(m) for m in messages]
    return await asyncio.gather(*tasks)

async def get_messages_by_user(user_id: int, skip: int = 0, limit: int = 10) -> List[dict]:
    # ユーザーIDに基づいてメッセージを検索
    messages = await collection_message.find({"user_id": user_id}).skip(skip).limit(limit).to_list(length=limit)
    tasks = [serialize_messages_with_user_name(m) for m in messages]
    return await asyncio.gather(*tasks)

async def get_message_by_id(message_id: str) -> dict:
    # メッセージIDでメッセージを取得
    message = await collection_message.find_one({"_id": ObjectId(message_id)})
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    serialized_message = await serialize_messages_with_user_name(message)
    return serialized_message

async def update_message(message_id: str, context: Optional[str] = None, data: Optional[datetime] = None) -> dict:
    # メッセージIDでメッセージを更新
    update_data = {}
    if context:
        update_data["context"] = context
    if data:
        update_data["data"] = data

    result = await collection_message.update_one({"_id": ObjectId(message_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message updated successfully"}

async def delete_message(message_id: str) -> dict:
    # メッセージIDでメッセージを削除
    result = await collection_message.delete_one({"_id": ObjectId(message_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message deleted successfully"}
