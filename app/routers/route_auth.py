from fastapi import APIRouter, Depends, HTTPException,Response, Request

from app.schemas.schema_user import UserBase, UserInfo
from app.schemas.schema_util import SuccessMessage
from app.auth_utils import AuthJwtCsrf

from app.database.db_auth import db_login,db_signup
from fastapi.encoders import jsonable_encoder



router = APIRouter()
auth = AuthJwtCsrf()

@router.post("/api/signup", response_model=UserInfo)
async def signup(response: Response, user: UserBase):
    user = jsonable_encoder(user)
    new_user = await db_signup(user)
    token = await db_login(user)  # ユーザー登録後、ログイン処理を行う
    response.set_cookie(key="access_token", value=token, httponly=True)
    return new_user

@router.post("/api/login", response_model=SuccessMessage)
async def login(response: Response, user: UserBase):
    user_data = jsonable_encoder(user)
    token, user_id = await db_login(user_data)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return {"message": "Login successful", "user_id": user_id}


