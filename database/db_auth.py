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
collection_user = database.user
auth = AuthJwtCsrf()


def user_serializer(user) ->dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"]
    }




async def db_signup(data: dict) -> dict:
    email = data.get("email")
    password = data.get("password")
    overlap_user = await collection_user.find_one({"email": email})
    if overlap_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user = await collection_user.insert_one({"email":email, "password": auth.generate_hashed_pw(password)})
    new_user = await collection_user.find_one({"_id": user.inserted_id})
    return user_serializer(new_user)


async def db_login(data: dict) ->str:
  email = data.get("email")
  password = data.get("password")
  user = await collection_user.find_one({"email": email})
  if not user or not auth.verify_pw(password, user["password"]):
    raise HTTPException(status_code=401, detail="Invalid email or password")  
  token = auth.encode_jwt(user['email'])
  return token