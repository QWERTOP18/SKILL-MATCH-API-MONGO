from fastapi import APIRouter, HTTPException, Request, Response
from app.schemas.schema_util import SuccessMessage
from app.schemas.schema_message import MessageCreate, Message, MessageUpdate, MessageResponse
from typing import List
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from fastapi.encoders import jsonable_encoder

from app.database.db_message import (
    create_message,
    get_messages_by_project,
    get_messages_by_user,
    get_message_by_id,
    update_message,
    delete_message,
)

router = APIRouter()

# 新しいメッセージの作成
@router.post("/api/messages/", response_model=SuccessMessage, status_code=HTTP_201_CREATED)
async def create_message_endpoint(
    message: MessageCreate, 
    request: Request
):
    try:
        result = await create_message(
            user_id=message.user_id,
            project_id=message.project_id,
            context=message.context,
            data=message.data
        )
        return SuccessMessage(message="Message created successfully", data=result)
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

# プロジェクト単位でメッセージを取得
@router.get("/api/messages/project/{project_id}", response_model=List[MessageResponse])
async def get_messages_by_project_endpoint(
    project_id: str, 
    skip: int = 0, 
    limit: int = 10
):
    try:
        messages = await get_messages_by_project(project_id, skip, limit)
        return jsonable_encoder(messages)
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

# ユーザー単位でメッセージを取得
@router.get("/api/messages/user/{user_id}", response_model=List[MessageResponse])
async def get_messages_by_user_endpoint(
    user_id: str, 
    skip: int = 0, 
    limit: int = 10
):
    try:
        messages = await get_messages_by_user(user_id, skip, limit)
        return jsonable_encoder(messages)
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

# メッセージIDで特定のメッセージを取得
@router.get("/api/messages/{message_id}", response_model=MessageResponse)
async def get_message_by_id_endpoint(message_id: str):
    try:
        message = await get_message_by_id(message_id)
        return jsonable_encoder(message)
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

# メッセージを更新
@router.put("/api/messages/{message_id}", response_model=SuccessMessage)
async def update_message_endpoint(
    message_id: str, 
    message_update: MessageUpdate
):
    try:
        result = await update_message(
            message_id=message_id, 
            context=message_update.context, 
            data=message_update.data
        )
        return SuccessMessage(message="Message updated successfully", data=result)
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

# メッセージを削除
@router.delete("/api/messages/{message_id}", response_model=SuccessMessage)
async def delete_message_endpoint(message_id: str):
    try:
        result = await delete_message(message_id)
        return SuccessMessage(message="Message deleted successfully", data=result)
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
