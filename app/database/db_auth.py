from decouple import config
import motor.motor_asyncio
from typing import Optional, Union
from bson import ObjectId
from fastapi import HTTPException 
import asyncio

from app.auth_utils import AuthJwtCsrf


MONGO_API_KEY = config("MONGO_API_KEY")


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
client.get_io_loop = asyncio.get_event_loop

database = client.API_DB
collection_task = database.task
collection_user = database.user
auth = AuthJwtCsrf()


def auth_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user.get("name", "no name"),
        "technical_skill": user.get("technical_skill", 0),
        "problem_solving_ability": user.get("problem_solving_ability", 0),
        "communication_skill": user.get("communication_skill", 0),
        "security_awareness": user.get("security_awareness", 0),
        "leadership_and_collaboration": user.get("leadership_and_collaboration", 0),
        "frontend_skill": user.get("frontend_skill", 0),
        "backend_skill": user.get("backend_skill", 0),
        "infrastructure_skill": user.get("infrastructure_skill", 0),
    }

async def db_signup(data: dict) -> dict:
    email = data.get("email")
    password = data.get("password")
    overlap_user = await collection_user.find_one({"email": email})
    if overlap_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user = await collection_user.insert_one({"email":email, "password": auth.generate_hashed_pw(password), "technical_skill":0, "problem_solving_ability":0, "communication_skill":0, "security_awareness":0, "leadership_and_collaboration":0, "frontend_skill":0, "backend_skill":0, "infrastructure_skill":0})
    new_user = await collection_user.find_one({"_id": user.inserted_id})
    return auth_serializer(new_user)


async def db_login(data: dict) -> tuple:
    email = data.get("email")
    password = data.get("password")
    user = await collection_user.find_one({"email": email})
    if not user or not auth.verify_pw(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = auth.encode_jwt(user["email"])
    return token, str(user["_id"])