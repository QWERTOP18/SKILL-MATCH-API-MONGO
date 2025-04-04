from decouple import config
import motor.motor_asyncio
from typing import Optional, Union
from bson import ObjectId
from fastapi import HTTPException 
import asyncio

from app.auth_utils import AuthJwtCsrf
from .db_task import task_serializer


MONGO_API_KEY = config("MONGO_API_KEY")


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
client.get_io_loop = asyncio.get_event_loop
database = client.API_DB

collection_user = database.user

auth = AuthJwtCsrf()

def user_serializer(user: dict) -> dict:
    """MongoDB のプロジェクトデータをシリアライズ"""
    return {
        "id": str(user["_id"]),
        "name": user.get("name", "no name"),
        "email": user["email"],
        # "password": user["password"],
        "technical_skill": user.get("technical_skill", 0),
        "problem_solving_ability": user.get("problem_solving_ability", 0),
        "communication_skill": user.get("communication_skill", 0),
        "security_awareness": user.get("security_awareness", 0),
        "leadership_and_collaboration": user.get("leadership_and_collaboration", 0),
        "frontend_skill": user.get("frontend_skill", 0),
        "backend_skill": user.get("backend_skill", 0),
        "infrastructure_skill": user.get("infrastructure_skill", 0),
    }




async def db_get_single_user(id: str) -> list:
    """MongoDB のプロジェクトデータを取得"""
    user = await collection_user.find_one({"_id": ObjectId(id)})
    if user:
        return user_serializer(user)
    else:
        raise HTTPException(status_code=404, detail="User not found")
    

async def db_update_user(id: str, update_data: dict) -> dict:
    # パスワード更新がある場合はハッシュ化する
    if "password" in update_data and update_data["password"]:
        update_data["password"] = auth.generate_hashed_pw(update_data["password"])
    result = await collection_user.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.modified_count == 1:
        new_user = await collection_user.find_one({"_id": ObjectId(id)})
        return user_serializer(new_user)
    raise HTTPException(status_code=404, detail="user not found")
