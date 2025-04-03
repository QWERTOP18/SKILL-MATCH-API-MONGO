from fastapi import APIRouter, Depends, HTTPException,Response, Request

from schemas import UserAuthBody, UserInfo, SuccessMessage
from auth_utils import AuthJwtCsrf

from database.db_auth import db_login,db_signup
from fastapi.encoders import jsonable_encoder



router = APIRouter()
auth = AuthJwtCsrf()

@router.post("/api/signup", response_model = UserInfo)
async def signup(user: UserAuthBody):
    user = jsonable_encoder(user)
    new_user = await db_signup(user)
    return new_user

@router.post("/api/login" ,response_model=SuccessMessage)
async def login(response: Response, user: UserAuthBody):
    user = jsonable_encoder(user)
    token = await db_login(user)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return {"message": "Login successful"}
    
    
