from fastapi import APIRouter, Depends, HTTPException,Response, Request

from schemas.schema_user import UserBase, UserInfo, User, UserBody
from schemas.schema_util import SuccessMessage
from auth_utils import AuthJwtCsrf

from database.db_user import db_get_single_user, db_update_user
from fastapi.encoders import jsonable_encoder



router = APIRouter()
auth = AuthJwtCsrf()


    
@router.get("/api/user/{id}", response_model=User)
async def get_single_user(id:str):
    res = await db_get_single_user(id)
    if res:
        return res
    raise HTTPException(
        status_code=404, detail = f"user with id {id} not found"
    )

@router.put("/api/user/{id}", response_model=User)
async def update_user(id:str, data:UserBody):
    res = await db_update_user(id, data)
    if res:
        return res
    raise HTTPException(
        status_code=404, detail = f"user with id {id} not found"
    )

