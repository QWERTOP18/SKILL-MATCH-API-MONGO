from fastapi import APIRouter, Depends, HTTPException, Response, Request
from app.schemas.schema_user import UserBase, User, UserBody, UserUpdate
from app.schemas.schema_util import SuccessMessage
from app.auth_utils import AuthJwtCsrf
from app.database.db_user import db_get_single_user, db_update_user, db_get_users_by_name
from fastapi.encoders import jsonable_encoder

router = APIRouter()
auth = AuthJwtCsrf()

@router.get("/api/user", response_model=list)
async def get_users_by_name(name: str):
    """
    クエリパラメーター 'name' に一致するユーザーの user_id と name を返します。
    """
    return await db_get_users_by_name(name)

@router.get("/api/user/{id}", response_model=User)
async def get_single_user(id: str):
    res = await db_get_single_user(id)
    if res:
        return res
    raise HTTPException(status_code=404, detail="user not found")

@router.put("/api/user/{id}", response_model=User)
async def update_user(id: str, data: UserUpdate):
    update_data = jsonable_encoder(data, exclude_none=True)
    res = await db_update_user(id, update_data)
    if res:
        return res
    raise HTTPException(status_code=404, detail="user not found")

