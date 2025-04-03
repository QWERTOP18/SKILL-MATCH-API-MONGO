from fastapi import APIRouter, Depends, HTTPException,Response, Request

from shemas import UserInfo, UserBody, SuccessMessage
from auth_utils import AuthJwtCsrf

from database import db_login,db_signup
from fastapi.encoders import jsonable_encoder



router = APIRouter()
auth = AuthJwtCsrf()

@router.post("/api/register", response_model = UserInfo)
async def signup(user: UserBody):
    user = jsonable_encoder(user)
    new_user = await db_signup(user)
    return new_user

@router.post("/api/login" ,response_model=SuccessMessage)
async def login(response: Response, user: UserBody):
    user = jsonable_encoder(user)
    token = await db_login(user)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return {"message": "Login successful"}
    
    
